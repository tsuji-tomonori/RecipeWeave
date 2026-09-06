"""必須の実DB試験を、スキップや空のJUnitだけで成功扱いにしない。"""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def verify(path: Path) -> None:
    root = ET.fromstring(path.read_text())
    cases = root.findall(".//testcase")
    if not cases or any(case.find("skipped") is not None for case in cases):
        raise ValueError("必須試験が未実行またはスキップされています")
    if any(case.find("failure") is not None or case.find("error") is not None for case in cases):
        raise ValueError("必須試験に失敗があります")
    print(f"必須試験{len(cases)}件の実行と成功を確認しました")


if __name__ == "__main__":
    verify(Path(sys.argv[1]))
