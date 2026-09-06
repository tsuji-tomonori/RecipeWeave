"""構築場所に依存しない配備資材とwheelメタデータの整合性を確認する。"""

import base64
import csv
import hashlib
from pathlib import Path

import pytest

from backend.tools.package_lambda import file_hashes, normalize_entrypoints


def installed_script(target: Path, interpreter: str) -> Path:
    (target / "bin").mkdir(parents=True)
    metadata = target / "example-1.0.dist-info"
    metadata.mkdir()
    script = target / "bin/example"
    script.write_text(f"#!{interpreter}\nprint('例')\n")
    (metadata / "RECORD").write_text(
        "bin/example,sha256=before,1\nexample-1.0.dist-info/RECORD,,\n"
    )
    return script


def test_build_directory_does_not_change_deployable_bytes(tmp_path: Path) -> None:
    """異なるPythonの設置場所でも、起動処理とRECORDを含む全資材が一致する。"""
    first, second = tmp_path / "local", tmp_path / "ci"
    installed_script(first, "/workspace/example/.venv/bin/python3")
    installed_script(second, "/home/runner/work/example/.venv/bin/python3")
    normalize_entrypoints(first)
    normalize_entrypoints(second)
    assert file_hashes(first) == file_hashes(second)
    script = (first / "bin/example").read_bytes()
    assert script == "#!/usr/bin/env python3.12\nprint('例')\n".encode()
    with (first / "example-1.0.dist-info/RECORD").open(newline="") as stream:
        row = next(csv.reader(stream))
    expected = base64.urlsafe_b64encode(hashlib.sha256(script).digest()).decode().rstrip("=")
    assert row == ["bin/example", f"sha256={expected}", str(len(script))]
    previous = file_hashes(first)
    normalize_entrypoints(first)
    assert file_hashes(first) == previous


@pytest.mark.parametrize(
    "name", ["__pycache__/example.cpython-312.pyc", "example.pyc", "example.pyo"]
)
def test_deployment_rejects_transient_bytecode(tmp_path: Path, name: str) -> None:
    """importや設定変更で一時bytecodeが混入した場合は配備資材として受け付けない。"""
    path = tmp_path / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"temporary-bytecode")
    with pytest.raises(ValueError, match="一時bytecode"):
        file_hashes(tmp_path)


def test_entrypoint_without_integrity_record_is_rejected(tmp_path: Path) -> None:
    """修正対象の起動スクリプトに整合するRECORDがなければ構築を止める。"""
    installed_script(tmp_path, "/workspace/example/.venv/bin/python3")
    (tmp_path / "example-1.0.dist-info/RECORD").unlink()
    with pytest.raises(ValueError, match="対応するRECORD"):
        normalize_entrypoints(tmp_path)
