from typing import Literal

from app.core.models import WireModel


class HealthResponse(WireModel):
    status: Literal["ok"] = "ok"
    catalog: Literal["sample"] = "sample"
    cloud_sync: Literal["not-deployed"] = "not-deployed"
