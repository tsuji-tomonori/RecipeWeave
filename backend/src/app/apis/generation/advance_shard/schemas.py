"""生成ワーカー操作の具体的な入力契約。"""

from typing import Literal

from pydantic import BaseModel, ConfigDict

from app.entities.json_contracts import BigInteger
from app.entities.models import GenerationShardRow as GenerationShardRow


class Request(BaseModel):
    model_config = ConfigDict(extra="forbid")
    expected_fence: BigInteger
    next_ordinal: BigInteger
    state: Literal["running", "done"]
