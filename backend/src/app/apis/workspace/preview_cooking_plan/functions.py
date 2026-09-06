from app.core.cooking_plan_service import CookingPlanService, PlanRequest, PlanResponse


def execute(service: CookingPlanService, request: PlanRequest) -> PlanResponse:
    """献立の版と分量を検証して、永続化せず段取りを返す。"""
    return service.preview(request)
