"""生成物の所有範囲を固定し、全件検査してから更新する。"""

from pathlib import Path

from .common import DesignError

TOP_LEVEL = {"README.md", "REGISTRY.md", "MANIFEST.md", "service.md"}


def owned(name: str) -> bool:
    path = Path(name)
    return (
        not path.is_absolute()
        and ".." not in path.parts
        and (
            path.suffix == ".md"
            or (path.name == "interface.openapi.json" and path.parts[0] == "api")
        )
        and (name in TOP_LEVEL or path.parts[0] in {"api", "database"})
    )


def ensure_safe(path: Path) -> None:
    for parent in [path, *path.parents]:
        if parent.is_symlink():
            raise DesignError(f"生成先にシンボリックリンクは使用できません: {path}")


def synchronize(directory: Path, outputs: dict[str, str], *, check: bool) -> None:
    """check時は一切書き込まない。既存の管理対象以外は削除しない。"""
    ensure_safe(directory)
    for name in outputs:
        if not owned(name):
            raise DesignError(f"管理対象外の出力です: {name}")
        ensure_safe(directory / name)
    existing = set()
    for path in directory.rglob("*"):
        relative = str(path.relative_to(directory))
        if relative.split("/")[0] in {"api", "database"} or relative in TOP_LEVEL:
            ensure_safe(path)
            if path.is_file():
                if not owned(relative):
                    raise DesignError(
                        f"生成専用ディレクトリに管理対象外のファイルがあります: {relative}"
                    )
                existing.add(relative)
    stale = existing - outputs.keys()
    changed = [
        name
        for name, text in outputs.items()
        if not (directory / name).is_file()
        or (directory / name).read_text(encoding="utf-8") != text
    ]
    if check:
        if stale or changed:
            raise DesignError(f"生成設計書に差分があります: {sorted(set(changed) | stale)}")
        return
    # 全入力と出力先を先に検査し、一時ファイルから各ファイルを置換する。
    for name in sorted(changed):
        path = directory / name
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".tmp")
        ensure_safe(temporary)
        temporary.write_text(outputs[name], encoding="utf-8")
        temporary.replace(path)
    for name in sorted(stale):
        (directory / name).unlink()
