"""生成ワーカー操作の具体的な入力契約。"""

from pydantic import BaseModel, ConfigDict, Field

from app.entities.json_contracts import BigInteger
from app.entities.models import GenerationShardRow as GenerationShardRow


class Request(BaseModel):
    model_config = ConfigDict(extra="forbid")
    expected_fence: BigInteger
    lease_seconds: int = Field(default=120, ge=30, le=3600)
