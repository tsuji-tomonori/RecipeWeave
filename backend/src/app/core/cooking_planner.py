"""工程依存関係・器具容量・作業者一人を守る決定的な調理計画を構成する。"""

from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from decimal import ROUND_CEILING, Decimal, InvalidOperation
from uuid import UUID

type Row = Mapping[str, object]
type Key = tuple[UUID, UUID]
type Interval = tuple[int, int, int]


@dataclass(frozen=True)
class PlannedTask:
    """開始・終了は計画開始からの秒数、予約数量は器具の台数。"""

    item_id: UUID
    step_id: UUID
    start: int
    end: int
    reservations: list[tuple[UUID, int]]


@dataclass(frozen=True)
class _Step:
    key: Key
    position: int
    number: int
    duration: int
    attention: str


@dataclass(frozen=True)
class _Dependency:
    before: Key
    minimum: int
    maximum: int | None


@dataclass(frozen=True)
class _Resource:
    id: UUID
    type_id: UUID
    quantity: int
    capacity: Decimal | None
    name: str
    code: str


@dataclass(frozen=True)
class _Requirement:
    type_id: UUID
    quantity: int
    capacity: Decimal | None
    exclusive: bool
    name: str


def _uuid(value: object) -> UUID:
    if isinstance(value, UUID):
        return value
    if not isinstance(value, str):
        raise ValueError("工程・器具の識別子が不正です。")
    try:
        return UUID(value)
    except ValueError as error:
        raise ValueError("工程・器具の識別子が不正です。") from error


def _decimal(value: object, name: str, *, positive: bool = True) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, int | float | str | Decimal):
        raise ValueError(f"{name}が確定していません。")
    try:
        result = Decimal(str(value))
    except InvalidOperation as error:
        raise ValueError(f"{name}が不正です。") from error
    if not result.is_finite() or result < 0 or (positive and result == 0):
        raise ValueError(f"{name}が不正です。")
    return result


def _integer(value: object, name: str, *, positive: bool = False) -> int:
    number = _decimal(value, name, positive=positive)
    if number != number.to_integral_value():
        raise ValueError(f"{name}は整数で指定してください。")
    return int(number)


def _duration(row: Row) -> int:
    base = _decimal(row.get("base_servings"), "基準人数")
    servings = _decimal(row.get("servings"), "人数")
    nominal = _integer(row.get("duration_max_s"), "基準所要時間")
    minimum = row.get("min_servings")
    maximum = row.get("max_servings")
    if minimum is not None and servings < _decimal(minimum, "人数下限"):
        raise ValueError("この人数は調理条件の検証範囲を下回っています。")
    if maximum is not None and servings > _decimal(maximum, "人数上限"):
        raise ValueError("この人数は調理条件の検証範囲を超えています。")
    mode = row.get("scaling_mode")
    if mode == "linear":
        factor = servings / base
    elif mode in {"fixed_batch", "capacity_batch"}:
        capacity = _decimal(row.get("batch_capacity"), "一回に調理できる人数")
        before = (base / capacity).to_integral_value(rounding=ROUND_CEILING)
        after = (servings / capacity).to_integral_value(rounding=ROUND_CEILING)
        factor = after / before
    elif mode in {"manual", "validated_curve"}:
        if servings != base:
            raise ValueError("この人数の調理時間は未確認です。基準人数へ戻してください。")
        factor = Decimal(1)
    else:
        raise ValueError("所要時間の換算規則を解釈できません。")
    return int((Decimal(nominal) * factor).to_integral_value(rounding=ROUND_CEILING))


def _steps(rows: Sequence[Row]) -> dict[Key, _Step]:
    result: dict[Key, _Step] = {}
    for row in rows:
        key = (_uuid(row.get("item_id")), _uuid(row.get("step_id")))
        attention = str(row.get("attention"))
        if key in result or attention not in {"active", "monitored", "passive"}:
            raise ValueError("工程が重複しているか、注意の区分が不正です。")
        result[key] = _Step(
            key,
            _integer(row.get("position"), "献立の順番"),
            _integer(row.get("step_no"), "工程の順番", positive=True),
            _duration(row),
            attention,
        )
    if not result:
        raise ValueError("献立に調理する工程がありません。")
    return result


def _dependencies(rows: Sequence[Row], steps: Mapping[Key, _Step]) -> dict[Key, list[_Dependency]]:
    result: dict[Key, list[_Dependency]] = defaultdict(list)
    for row in rows:
        item = _uuid(row.get("item_id"))
        before = (item, _uuid(row.get("before_step_id")))
        after = (item, _uuid(row.get("after_step_id")))
        if before not in steps or after not in steps or before == after:
            raise ValueError("依存関係が存在しない工程を参照しています。")
        if row.get("kind") not in {"material", "sequence", "safety", "quality"}:
            raise ValueError("工程の依存関係を解釈できません。")
        minimum = _integer(row.get("min_lag_s"), "最小待ち時間")
        maximum = row.get("max_lag_s")
        latest = None if maximum is None else _integer(maximum, "最大待ち時間")
        if latest is not None and latest < minimum:
            raise ValueError("最大待ち時間が最小待ち時間を下回っています。")
        result[after].append(_Dependency(before, minimum, latest))
    remaining = set(steps)
    while remaining:
        ready = {key for key in remaining if all(d.before not in remaining for d in result[key])}
        if not ready:
            raise ValueError("工程の依存関係が循環しています。")
        remaining -= ready
    return result


def _resources(rows: Sequence[Row]) -> list[_Resource]:
    resources: list[_Resource] = []
    ids: set[UUID] = set()
    for row in rows:
        resource_id = _uuid(row.get("id"))
        if resource_id in ids:
            raise ValueError("器具の識別子が重複しています。")
        ids.add(resource_id)
        capacity = row.get("capacity")
        resources.append(
            _Resource(
                resource_id,
                _uuid(row.get("resource_type_id")),
                _integer(row.get("quantity"), "器具の台数", positive=True),
                None if capacity is None else _decimal(capacity, "器具の容量"),
                str(row.get("name", "器具")),
                str(row.get("code", "")),
            )
        )
    return sorted(
        resources, key=lambda resource: (resource.capacity or Decimal(0), str(resource.id))
    )


def _requirements(rows: Sequence[Row]) -> dict[UUID, list[_Requirement]]:
    result: dict[UUID, list[_Requirement]] = defaultdict(list)
    for row in rows:
        capacity = row.get("capacity_min")
        exclusive = row.get("exclusive", False)
        if not isinstance(exclusive, bool):
            raise ValueError("器具の占有条件が不正です。")
        result[_uuid(row.get("step_id"))].append(
            _Requirement(
                _uuid(row.get("resource_type_id")),
                _integer(row.get("quantity"), "必要な器具の台数", positive=True),
                None if capacity is None else _decimal(capacity, "必要な器具の容量"),
                exclusive,
                str(row.get("name", "器具")),
            )
        )
    return result


def _peak(intervals: Sequence[Interval], start: int, end: int) -> int:
    events: dict[int, int] = defaultdict(int)
    if start == end:
        return 0
    for left, right, quantity in intervals:
        if right <= start or left >= end:
            continue
        events[max(left, start)] += quantity
        events[min(right, end)] -= quantity
    current = peak = 0
    for time in sorted(events):
        current += events[time]
        peak = max(peak, current)
    return peak


def _allocate(
    requirements: Sequence[_Requirement],
    resources: Sequence[_Resource],
    calendar: Mapping[UUID, list[Interval]],
    start: int,
    end: int,
) -> list[tuple[UUID, int]] | None:
    reservations: dict[UUID, int] = defaultdict(int)
    for requirement in requirements:
        needed = requirement.quantity
        for resource in resources:
            if resource.type_id != requirement.type_id:
                continue
            if requirement.capacity is not None and (
                resource.capacity is None or resource.capacity < requirement.capacity
            ):
                continue
            available = resource.quantity - _peak(calendar.get(resource.id, []), start, end)
            available -= reservations[resource.id]
            if requirement.exclusive and available != resource.quantity:
                continue
            used = min(needed, available)
            if used <= 0:
                continue
            reservations[resource.id] += resource.quantity if requirement.exclusive else used
            needed -= used
            if needed == 0:
                break
        if needed:
            return None
    return [(resource_id, quantity) for resource_id, quantity in reservations.items() if quantity]


def _earliest(
    step: _Step,
    earliest: int,
    latest: int | None,
    requirements: Sequence[_Requirement],
    resources: Sequence[_Resource],
    calendar: Mapping[UUID, list[Interval]],
    operator: Sequence[Interval],
) -> tuple[int, list[tuple[UUID, int]]]:
    if _allocate(requirements, resources, {}, 0, step.duration) is None:
        raise ValueError("必要な台数・容量を満たす器具がありません。器具の設定を確認してください。")
    boundaries = {earliest}
    boundaries.update(
        end for intervals in calendar.values() for _, end, _ in intervals if end >= earliest
    )
    boundaries.update(end for _, end, _ in operator if end >= earliest)
    for start in sorted(boundaries):
        if latest is not None and start > latest:
            break
        end = start + step.duration
        if step.attention != "passive" and _peak(operator, start, end):
            continue
        allocated = _allocate(requirements, resources, calendar, start, end)
        if allocated is not None:
            return start, allocated
    raise ValueError(
        "この割り当てでは最大待ち時間を守れません。献立や器具の構成を見直してください。"
    )


def build_plan(
    steps: Sequence[Row],
    dependencies: Sequence[Row],
    requirements: Sequence[Row],
    resources: Sequence[Row],
) -> list[PlannedTask]:
    """待ち時間上限を優先する非割込み計画。成立しない場合は時刻を捏造せず拒否する。"""
    tasks = _steps(steps)
    parents = _dependencies(dependencies, tasks)
    available = _resources(resources)
    demands = _requirements(requirements)
    known_steps = {key[1] for key in tasks}
    if set(demands) - known_steps:
        raise ValueError("器具の条件が存在しない工程を参照しています。")
    calendar: dict[UUID, list[Interval]] = defaultdict(list)
    operator: list[Interval] = []
    planned: dict[Key, PlannedTask] = {}
    while len(planned) < len(tasks):
        candidates: list[tuple[int, int, int, int, str, _Step, list[tuple[UUID, int]]]] = []
        for key, task in tasks.items():
            if key in planned or any(parent.before not in planned for parent in parents[key]):
                continue
            lower = max((planned[d.before].end + d.minimum for d in parents[key]), default=0)
            deadlines = [
                planned[d.before].end + d.maximum for d in parents[key] if d.maximum is not None
            ]
            upper = min(deadlines) if deadlines else None
            demand = list(demands[task.key[1]])
            people = [resource for resource in available if resource.code == "person"]
            if task.attention != "passive":
                if not people:
                    raise ValueError("作業者の設定がありません。調理する人を一人設定してください。")
                person_type = people[0].type_id
                if not any(requirement.type_id == person_type for requirement in demand):
                    demand.append(_Requirement(person_type, 1, None, False, "作業者"))
            start, allocation = _earliest(task, lower, upper, demand, available, calendar, operator)
            candidates.append(
                (
                    upper if upper is not None else 2**63 - 1,
                    start,
                    task.position,
                    task.number,
                    str(key),
                    task,
                    allocation,
                )
            )
        if not candidates:
            raise ValueError("工程の依存関係を解決できません。")
        _, start, _, _, _, selected, reservations = min(candidates, key=lambda item: item[:5])
        end = start + selected.duration
        planned[selected.key] = PlannedTask(*selected.key, start, end, reservations)
        for resource_id, quantity in reservations:
            calendar[resource_id].append((start, end, quantity))
        if selected.attention != "passive":
            operator.append((start, end, 1))
    return sorted(
        planned.values(),
        key=lambda task: (task.start, task.end, str(task.item_id), str(task.step_id)),
    )
