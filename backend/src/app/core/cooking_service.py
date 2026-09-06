"""DBの材料・工程・設備から調理を計画し、進捗と消費を原子的に保存する。"""

import hashlib
from collections import defaultdict
from decimal import Decimal
from typing import TYPE_CHECKING, Any, cast
from uuid import UUID, uuid4, uuid5

from fastapi import HTTPException
from psycopg.types.json import Jsonb

from app.core.models import AppSnapshot
from app.core.workspace_models import CookingRequest
from app.core.workspace_service import identifier, quantity
from app.entities.json_contracts import CookingInput

if TYPE_CHECKING:
    from app.core.workspace_service import WorkspaceService


class CookingService:
    """ワークスペースの排他版を使い、完了の再送で二重消費しない。"""

    def __init__(self, workspace: "WorkspaceService") -> None:
        self.workspace = workspace
        self.user_id = workspace.user_id

    def read_current(self) -> dict[str, Any] | None:
        """直近の計画をタスク・献立・消費台帳から復元する。"""
        q = self.workspace.queries("get_workspace")
        rows = q.run("q011_session", user_id=self.user_id)
        if not rows:
            return None
        session = rows[0]
        tasks = q.run("q012_tasks", session_id=session["id"])
        resources = q.run("q013_task_resources", session_id=session["id"])
        plan: list[dict[str, Any]] = []
        timers: list[dict[str, Any]] = []
        completed: list[str] = []
        for task in tasks:
            key = f"{task['menu_item_id']}:{task['step_id']}"
            plan.append(
                {
                    "id": str(task["step_id"]),
                    "key": key,
                    "mealItemId": str(task["menu_item_id"]),
                    "recipeId": str(task["recipe_id"]),
                    "recipeName": task["recipe_name"],
                    "title": task["title"] or "調理工程",
                    "instruction": task["instruction"],
                    "timeScalingMode": task["scaling_mode"],
                    "durationSource": task["duration_source"],
                    "confirmedDurationSeconds": task["confirmed_duration_s"],
                    "minutes": (task["planned_end_s"] - task["planned_start_s"]) / 60,
                    "mode": task["attention"],
                    "guide": None,
                    "equipment": [r["name"] for r in resources if r["task_id"] == task["id"]],
                    "startMinute": task["planned_start_s"] / 60,
                    "endMinute": task["planned_end_s"] / 60,
                }
            )
            if task["status"] == "completed":
                completed.append(key)
            if task["timer_started_at"] is not None:
                timers.append(
                    {
                        "stepKey": key,
                        "startedAt": task["timer_started_at"].timestamp() * 1000,
                        "durationSeconds": task["timer_duration_s"],
                    }
                )
        outcomes = {
            "applied": "使用量を反映しました",
            "not_requested": "在庫変更なしで完了",
            "insufficient": "在庫が不足しています。数量は変更していません",
            "unknown": "数量不明のため在庫は変更していません",
            "incompatible": "単位・形態を換算できないため在庫は変更していません",
        }
        results: list[dict[str, Any]] = []
        if session["status"] == "completed":
            for total in q.run("q014_totals", session_id=session["id"]):
                outcome = total["consumption_outcome"]
                results.append(
                    {
                        "foodId": str(total["food_id"]),
                        "form": total["form"],
                        "quantity": quantity(total["actual_amount"], total["unit"]),
                        "applied": outcome == "applied",
                        "reason": outcomes[outcome],
                        "lotIds": [
                            str(value) for value in cast(list[UUID], total["lot_ids"] or [])
                        ],
                    }
                )
        return {
            "id": str(session["id"]),
            "mealSnapshot": self.workspace.read_meal(q, session["menu_id"]),
            "plan": plan,
            "index": session["current_task_index"],
            "completedStepIds": completed,
            "timers": timers,
            "status": {
                "cooking": "active",
                "planned": "active",
                "paused": "paused",
                "completed": "completed",
            }[session["status"]],
            "consumptionResults": results,
        }

    def create(self, request: CookingRequest) -> AppSnapshot:
        """画面から送られた計画を信用せず、DBのDAGと設備で再計画する。"""
        from app.core.cooking_planner import build_plan

        q = self.workspace.begin("create_cooking_session", request)
        if q.run("q001_current", user_id=self.user_id):
            raise HTTPException(409, "調理中の料理を再開するか、完了してから始めてください")
        if not request.session.meal_snapshot:
            raise HTTPException(422, "調理する料理を選んでください")
        session_id = identifier(request.session.id)
        menu_id = uuid5(session_id, "frozen-menu")
        # 将来の献立編集が実行中の調理へ影響しないよう、専用の関連行を作る。
        frozen_ids: dict[str, UUID] = {}
        for item in request.session.meal_snapshot:
            frozen = item.model_copy(update={"id": str(uuid5(session_id, "item:" + item.id))})
            frozen_ids[item.id] = identifier(frozen.id)
            self.workspace.add_item(q, frozen, menu_id, "調理開始時の献立")
        steps = q.run("q020_steps", menu_id=menu_id)
        dependencies = q.run("q021_dependencies", menu_id=menu_id)
        requirements = q.run("q022_requirements", menu_id=menu_id)
        resources = q.run("q023_resources", user_id=self.user_id)
        try:
            estimates: list[dict[str, Any]] = []
            for estimate in request.duration_estimates:
                if estimate.meal_item_id not in frozen_ids:
                    raise ValueError("この献立に含まれない工程の見積りが指定されています。")
                estimates.append(
                    {
                        **estimate.model_dump(),
                        "meal_item_id": frozen_ids[estimate.meal_item_id],
                    }
                )
            plan = build_plan(
                steps, dependencies, requirements, resources, duration_estimates=estimates
            )
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc
        ingredients = q.run("q024_ingredients", menu_id=menu_id)
        if any(r["amount"] is None for r in ingredients):
            raise HTTPException(422, "調理前に材料の量を確定してください")
        identities: dict[tuple[UUID, UUID], set[UUID | None]] = defaultdict(set)
        for ingredient in ingredients:
            identities[(ingredient["form_id"], ingredient["unit_id"])].add(
                ingredient["product_version_id"]
            )
        if any(len(values) > 1 for values in identities.values()):
            raise HTTPException(422, "同じ食材の複数商品は、商品版ごとの調理APIで指定してください")
        revision = q.run("q030_menu_revision", menu_id=menu_id, user_id=self.user_id)[0]["revision"]
        item_values: dict[UUID, dict[str, Any]] = {}
        for row in ingredients:
            item_values[row["item_id"]] = {
                "id": row["item_id"],
                "recipe_version_id": row["recipe_version_id"],
                "servings": row["servings"],
            }
        snapshot = CookingInput.model_validate(
            {
                "schema_version": 1,
                "menu_revision": revision,
                "items": list(item_values.values()),
                "ingredients": [
                    {
                        "id": r["ingredient_id"],
                        "form_id": r["form_id"],
                        "amount": r["amount"],
                        "unit_id": r["unit_id"],
                        "conversion_id": r["conversion_id"],
                    }
                    for r in ingredients
                ],
                "resources": [
                    {key: r[key] for key in ["id", "resource_type_id", "quantity", "capacity"]}
                    for r in resources
                ],
                "planner_config": {
                    "planner_version": "dag-resource-manual-v2",
                    "concurrent_active_tasks": 1,
                },
            }
        )
        encoded = snapshot.model_dump_json()
        q.run(
            "q025_session",
            session_id=session_id,
            menu_id=menu_id,
            revision=revision,
            snapshot=Jsonb(snapshot.model_dump(mode="json")),
            hash=hashlib.sha256(encoded.encode()).hexdigest(),
        )
        task_ids: dict[tuple[UUID, UUID], UUID] = {}
        for task in plan:
            task_id = uuid5(session_id, f"task:{task.item_id}:{task.step_id}")
            task_ids[(task.item_id, task.step_id)] = task_id
            q.run(
                "q026_task",
                row_id=task_id,
                session_id=session_id,
                item_id=task.item_id,
                step_id=task.step_id,
                start=task.start,
                end=task.end,
                duration_source=task.duration_source,
                confirmed_duration_s=task.confirmed_duration_s,
            )
            for resource_id, count in task.reservations:
                q.run(
                    "q028_reservation",
                    row_id=uuid4(),
                    task_id=task_id,
                    resource_id=resource_id,
                    start=task.start,
                    end=task.end,
                    quantity=count,
                )
        for dependency in dependencies:
            q.run(
                "q027_dependency",
                row_id=uuid4(),
                before_id=task_ids[(dependency["item_id"], dependency["before_step_id"])],
                after_id=task_ids[(dependency["item_id"], dependency["after_step_id"])],
                min_lag=dependency["min_lag_s"],
                max_lag=dependency["max_lag_s"],
                reason=dependency["kind"],
            )
        totals: dict[tuple[UUID, UUID | None, UUID], Decimal] = defaultdict(Decimal)
        for ingredient in ingredients:
            key = (ingredient["form_id"], ingredient["product_version_id"], ingredient["unit_id"])
            totals[key] += ingredient["amount"]
        for (form_id, product_id, unit_id), amount in totals.items():
            q.run(
                "q029_total",
                row_id=uuid4(),
                session_id=session_id,
                form_id=form_id,
                product_id=product_id,
                unit_id=unit_id,
                amount=amount,
            )
        return self.workspace.finish(q)

    def update(self, request: CookingRequest, row_id: UUID) -> AppSnapshot:
        """本人の工程・タイマーだけを更新し、完了の確定と消費を同時に行う。"""
        if request.duration_estimates:
            raise HTTPException(
                422, "開始後の見積り時間は変更できません。新しい調理として計画してください"
            )
        q = self.workspace.begin("update_cooking_session", request)
        if identifier(request.session.id) != row_id:
            raise HTTPException(422, "調理IDが一致しません")
        current = q.run("q001_current", user_id=self.user_id)
        if not any(r["id"] == row_id for r in current):
            raise HTTPException(409, "調理がないか完了済みです")
        tasks = q.run("q002_tasks", session_id=row_id, user_id=self.user_id)
        by_key = {f"{t['menu_item_id']}:{t['step_id']}": t for t in tasks}
        completed = set(request.session.completed_step_ids)
        existing_completed = {
            key for key, value in by_key.items() if value["status"] == "completed"
        }
        if (
            not completed <= set(by_key)
            or not existing_completed <= completed
            or request.session.index > len(tasks)
        ):
            raise HTTPException(422, "工程の進捗が計画と一致しません")
        for key in completed - existing_completed:
            q.run("q004_complete_task", row_id=by_key[key]["id"], session_id=row_id)
        for timer in request.session.timers:
            if timer.step_key not in by_key:
                raise HTTPException(422, "タイマーの工程が見つかりません")
            # 開始時刻と時間はサーバーで採番し、利用者が送る時計値を採用しない。
            q.run("q005_timer", row_id=by_key[timer.step_key]["id"], session_id=row_id)
        status = {"active": "cooking", "paused": "paused", "completed": "completed"}[
            request.session.status
        ]
        if status == "completed":
            if completed != set(by_key):
                raise HTTPException(422, "すべての工程を確認してから完了してください")
            self._consume(q, request, row_id)
        if not q.run(
            "q003_progress",
            status=status,
            index=request.session.index,
            session_id=row_id,
            user_id=self.user_id,
        ):
            raise HTTPException(409, "調理の状態が変わりました")
        return self.workspace.finish(q)

    def _consume(self, q: Any, request: CookingRequest, session_id: UUID) -> None:
        totals = q.run("q006_totals", session_id=session_id)
        request_keys = [
            (r.food_id, r.form, r.quantity.unit) for r in request.session.consumption_results
        ]
        total_keys = [(str(r["food_id"]), r["form"], r["unit"]) for r in totals]
        # 商品版を省略する画面で複数商品へ同じ使用量を適用しない。
        if len(set(total_keys)) != len(total_keys):
            raise HTTPException(422, "同じ食材の複数商品・形態は個別の調理APIで指定してください")
        if len(set(request_keys)) != len(request_keys):
            raise HTTPException(422, "同じ食材の使用量を重複して指定できません")
        requested = {
            (r.food_id, r.form, r.quantity.unit): r.quantity.value
            for r in request.session.consumption_results
        }
        allowed = set(total_keys)
        if set(requested) - allowed:
            raise HTTPException(422, "料理に含まれない食材や単位は使用量に指定できません")
        # 同一ロットを複数需要が使う場合は、一度の台帳行へ集約する。
        ledger: dict[tuple[UUID, UUID], Decimal] = defaultdict(Decimal)
        for total in totals:
            key = (str(total["food_id"]), total["form"], total["unit"])
            supplied = requested.get(key, total["required_amount"])
            amount = Decimal(str(supplied)) if supplied is not None else None
            outcome = "not_requested"
            if request.deduct:
                if amount is None:
                    outcome = "unknown"
                else:
                    available = q.run(
                        "q007_available",
                        user_id=self.user_id,
                        form_id=total["form_id"],
                        unit_id=total["unit_id"],
                        product_id=total["product_version_id"],
                    )
                    if sum((r["amount"] for r in available), Decimal(0)) < amount:
                        outcome = "insufficient"
                    else:
                        remaining = amount
                        for lot in available:
                            used = min(remaining, lot["amount"])
                            if used > 0:
                                q.run(
                                    "q008_consume",
                                    lot_id=lot["id"],
                                    user_id=self.user_id,
                                    amount=used,
                                )
                                ledger[(lot["id"], total["unit_id"])] += used
                                remaining -= used
                            if remaining == 0:
                                break
                        outcome = "applied"
            q.run(
                "q010_outcome",
                total_id=total["id"],
                session_id=session_id,
                amount=amount,
                outcome=outcome,
            )
        for (lot_id, unit_id), amount in ledger.items():
            q.run(
                "q009_ledger",
                row_id=uuid5(session_id, "consume:" + str(lot_id)),
                user_id=self.user_id,
                session_id=session_id,
                lot_id=lot_id,
                amount=amount,
                unit_id=unit_id,
            )
