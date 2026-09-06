"""調理計画の依存関係・容量・人の予約と、未検証換算の拒否を検証する。"""

from copy import deepcopy
from decimal import Decimal
from uuid import UUID

import pytest

from app.core.cooking_planner import build_plan


def uid(value: int) -> UUID:
    return UUID(int=value)


def step(number: int, attention: str = "active", duration: int = 60) -> dict[str, object]:
    return {
        "item_id": uid(100),
        "step_id": uid(number),
        "recipe_id": uid(200),
        "step_no": number,
        "position": 1,
        "duration_max_s": duration,
        "attention": attention,
        "servings": Decimal(2),
        "base_servings": Decimal(2),
        "scaling_mode": "manual",
        "batch_capacity": None,
        "min_servings": Decimal(1),
        "max_servings": Decimal(12),
    }


def resource(
    number: int, kind: int, quantity: int = 1, capacity: int | None = None
) -> dict[str, object]:
    return {
        "id": uid(number),
        "resource_type_id": uid(kind),
        "quantity": quantity,
        "capacity": capacity,
        "name": "作業者" if kind == 500 else "鍋",
        "code": "person" if kind == 500 else "pot",
    }


def requirement(number: int, kind: int = 501, capacity: int | None = None) -> dict[str, object]:
    return {
        "step_id": uid(number),
        "resource_type_id": uid(kind),
        "quantity": 1,
        "capacity_min": capacity,
        "name": "鍋",
        "code": "pot",
    }


def dependency(
    before: int, after: int, minimum: int = 0, maximum: int | None = None
) -> dict[str, object]:
    return {
        "item_id": uid(100),
        "before_step_id": uid(before),
        "after_step_id": uid(after),
        "min_lag_s": minimum,
        "max_lag_s": maximum,
        "kind": "sequence",
    }


def kitchen() -> list[dict[str, object]]:
    return [resource(400, 500), resource(401, 501, capacity=2000)]


def test_active_and_monitored_reserve_one_person_even_without_explicit_requirement() -> None:
    """見守り工程を手放し待ちとして二重予約しない。"""
    result = build_plan([step(1), step(2, "monitored"), step(3)], [], [], kitchen())
    assert [(task.start, task.end) for task in result] == [(0, 60), (60, 120), (120, 180)]
    assert all((uid(400), 1) in task.reservations for task in result)


def test_passive_wait_can_overlap_active_work_but_keeps_appliance() -> None:
    """手放し待ちは他の手作業と重なるが、使用中の器具は開放しない。"""
    result = build_plan(
        [step(1, "passive", 180), step(2), step(3, "passive")],
        [],
        [requirement(1), requirement(3)],
        kitchen(),
    )
    by_id = {task.step_id: task for task in result}
    assert by_id[uid(1)].start == by_id[uid(2)].start == 0
    assert by_id[uid(3)].start >= by_id[uid(1)].end


def test_independent_menu_items_keep_separate_task_keys() -> None:
    """同じ料理を二皿作る場合も工程と予約を重複削除しない。"""
    first = step(1)
    second = {**first, "item_id": uid(101), "position": 2}
    result = build_plan([first, second], [], [], kitchen())
    assert {task.item_id for task in result} == {uid(100), uid(101)}
    assert result[1].start >= result[0].end


def test_capacity_is_per_appliance_and_unknown_capacity_is_not_assumed_sufficient() -> None:
    """容量不明や小さい鍋を、必要容量がある工程へ割り当てない。"""
    devices = [
        resource(400, 500),
        resource(401, 501, capacity=1000),
        resource(402, 501, capacity=3000),
        resource(403, 501),
    ]
    result = build_plan([step(1)], [], [requirement(1, capacity=2000)], devices)
    assert (uid(402), 1) in result[0].reservations
    assert (uid(401), 1) not in result[0].reservations
    with pytest.raises(ValueError, match="容量"):
        build_plan([step(1)], [], [requirement(1, capacity=5000)], devices)


def test_available_quantity_permits_parallel_passive_tasks_without_overbooking() -> None:
    """二台あれば二工程は並列化できるが、三つ目は器具が空くまで待つ。"""
    devices = [resource(400, 500), resource(401, 501, quantity=2)]
    result = build_plan(
        [step(1, "passive"), step(2, "passive"), step(3, "passive")],
        [],
        [requirement(1), requirement(2), requirement(3)],
        devices,
    )
    assert [task.start for task in result] == [0, 0, 60]


def test_nonoverlapping_reservations_do_not_sum_as_simultaneous_use() -> None:
    """異なる時間帯の既存予約を合計して、空き器具を過小評価しない。"""
    result = build_plan(
        [step(1, duration=60), step(2, duration=60), step(3, "passive", 120)],
        [dependency(1, 2)],
        [requirement(1), requirement(2), requirement(3)],
        [resource(400, 500), resource(401, 501, quantity=2)],
    )
    by_id = {task.step_id: task for task in result}
    assert by_id[uid(3)].start == 0
    assert by_id[uid(2)].start == 60


def test_exclusive_use_reserves_the_whole_named_resource_pool() -> None:
    """占有工程と別工程が同じ器具プールを同時に使わない。"""
    demands = [{**requirement(1), "exclusive": True}, requirement(2)]
    result = build_plan(
        [step(1, "passive"), step(2, "passive")],
        [],
        demands,
        [resource(400, 500), resource(401, 501, quantity=2)],
    )
    assert (uid(401), 2) in result[0].reservations
    assert result[1].start == 60


def test_dependency_minimum_lag_is_preserved() -> None:
    """先行工程が終わった直後でなく、最低待ち時間を守って開始する。"""
    result = build_plan([step(1), step(2)], [dependency(1, 2, 30, 90)], [], kitchen())
    assert result[1].start == result[0].end + 30


def test_impossible_deadline_is_rejected_instead_of_dropping_constraint() -> None:
    """品質上の最大待ち時間を超える計画を成功として返さない。"""
    with pytest.raises(ValueError, match="最大待ち時間"):
        build_plan(
            [step(1, "passive", 10), step(2, duration=100), step(3)],
            [dependency(1, 2), dependency(1, 3, 0, 0), dependency(2, 3)],
            [],
            kitchen(),
        )


@pytest.mark.parametrize("edges", [[dependency(1, 2), dependency(2, 1)], [dependency(1, 3)]])
def test_cycles_and_missing_predecessors_are_rejected(edges: list[dict[str, object]]) -> None:
    """循環や存在しない工程の参照を、その場で拒否する。"""
    with pytest.raises(ValueError, match="循環|存在しない"):
        build_plan([step(1), step(2)], edges, [], kitchen())


def test_linear_and_capacity_batch_rules_scale_duration_with_rounding() -> None:
    """比例とバッチの所要時間換算を区別し、秒未満は切り上げる。"""
    linear = {**step(1, duration=61), "servings": Decimal(3), "scaling_mode": "linear"}
    batch = {
        **step(2),
        "servings": Decimal(5),
        "scaling_mode": "capacity_batch",
        "batch_capacity": Decimal(2),
    }
    result = build_plan([linear, batch], [], [], kitchen())
    assert result[0].end - result[0].start == 92
    assert result[1].end - result[1].start == 180


@pytest.mark.parametrize("mode", ["manual", "validated_curve"])
def test_unverified_time_for_changed_servings_is_rejected(mode: str) -> None:
    """検証点や手動確認が無い人数変更で加熱時間を推測しない。"""
    with pytest.raises(ValueError, match="未確認"):
        build_plan([{**step(1), "servings": Decimal(3), "scaling_mode": mode}], [], [], kitchen())


@pytest.mark.parametrize("value", [None, -1, Decimal("NaN"), Decimal("Infinity")])
def test_unknown_or_nonfinite_duration_is_rejected(value: object) -> None:
    """不明・負数・非有限の時間をゼロ等で埋めない。"""
    with pytest.raises(ValueError):
        build_plan([{**step(1), "duration_max_s": value}], [], [], kitchen())


def test_input_data_is_not_modified_and_result_is_deterministic() -> None:
    """同じ正規化入力から同じ計画を生成し、入力行へ計画を書き込まない。"""
    rows = [step(1), step(2)]
    original = deepcopy(rows)
    first = build_plan(rows, [], [], kitchen())
    assert first == build_plan(rows, [], [], kitchen())
    assert rows == original


def test_missing_operator_is_rejected() -> None:
    """台所の作業者を設定せずに手作業や見守りを開始しない。"""
    with pytest.raises(ValueError, match="作業者"):
        build_plan([step(1, "monitored")], [], [], [resource(401, 501)])


def estimate(number: int, seconds: object = 90) -> dict[str, object]:
    return {"meal_item_id": uid(100), "step_id": uid(number), "duration_seconds": seconds}


def test_three_servings_use_confirmed_manual_duration_and_keep_dependencies() -> None:
    rows = [{**step(1), "servings": 3}, {**step(2), "servings": 3}]
    result = build_plan(
        rows,
        [dependency(1, 2, 15)],
        [],
        kitchen(),
        duration_estimates=[estimate(1, 90), estimate(2, 120)],
    )
    assert [(task.start, task.end) for task in result] == [(0, 90), (105, 225)]
    assert all(task.duration_source == "user_estimate" for task in result)
    assert [task.confirmed_duration_s for task in result] == [90, 120]


@pytest.mark.parametrize("value", [0, -1, 1.5, True, None, "NaN", "Infinity", 86401])
def test_invalid_user_duration_is_rejected(value: object) -> None:
    with pytest.raises(ValueError):
        build_plan(
            [{**step(1), "servings": 3}], [], [], kitchen(), duration_estimates=[estimate(1, value)]
        )


def test_manual_estimate_cannot_override_another_mode_or_unknown_step() -> None:
    with pytest.raises(ValueError, match="手動"):
        build_plan(
            [{**step(1), "scaling_mode": "linear"}],
            [],
            [],
            kitchen(),
            duration_estimates=[estimate(1)],
        )
    with pytest.raises(ValueError, match="含まれない"):
        build_plan([step(1)], [], [], kitchen(), duration_estimates=[estimate(2)])
    with pytest.raises(ValueError, match="重複"):
        build_plan([step(1)], [], [], kitchen(), duration_estimates=[estimate(1), estimate(1)])


def test_confirmed_time_cannot_bypass_serving_limit_or_known_capacity() -> None:
    with pytest.raises(ValueError, match="人数.*範囲"):
        build_plan(
            [{**step(1), "servings": 13}], [], [], kitchen(), duration_estimates=[estimate(1)]
        )
    with pytest.raises(ValueError, match="容量"):
        build_plan(
            [{**step(1), "servings": 3}],
            [],
            [requirement(1, capacity=3000)],
            kitchen(),
            duration_estimates=[estimate(1)],
        )


def test_each_changed_manual_step_requires_confirmation() -> None:
    with pytest.raises(ValueError, match="未確認"):
        build_plan(
            [{**step(1), "servings": 3}, {**step(2), "servings": 3}],
            [],
            [],
            kitchen(),
            duration_estimates=[estimate(1)],
        )
