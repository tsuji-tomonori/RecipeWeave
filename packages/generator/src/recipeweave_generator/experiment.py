"""検証用データを評価する前に、評価手順と盲検化した割り当てを固定する。"""

import hashlib
import json
import random
from pathlib import Path

from .export import atomic_json
from .space import Space


def prepare(root: Path) -> None:
    output = root / "experiments/confirmation"
    if output.exists():
        raise ValueError("confirmation assignments already exist; never resample after judging")
    output.mkdir(parents=True)
    pilot = json.loads((root / "experiments/pilot/design.json").read_text())
    excluded = set(pilot["ordinals"])
    samples = []
    versions = {}
    for cohort, file, seed in [
        ("baseline", "v2_baseline.json", 916203),
        ("revised", "v3_reviewed.json", 723401),
    ]:
        space = Space.load(root / "data/catalog" / file)
        rng = random.Random(seed)
        ordinals = []
        used = set(excluded) if cohort == "baseline" else set()
        while len(ordinals) < 400:
            n = rng.randrange(space.total)
            if n in used:
                continue
            used.add(n)
            ordinals.append(n)
        versions[cohort] = {
            "definition_sha256": space.digest,
            "seed": seed,
            "n": 400,
            "population": space.total - (len(excluded) if cohort == "baseline" else 0),
        }
        samples.extend({"cohort": cohort, "ordinal": n, **space.describe(n)} for n in ordinals)
    random.Random(128975).shuffle(samples)
    for i, row in enumerate(samples):
        row["id"] = f"C{i:04d}"
    atomic_json(output / "samples_key.json", samples)
    blinded = [{k: v for k, v in row.items() if k not in {"cohort", "ordinal"}} for row in samples]
    atomic_json(output / "blind_0.json", blinded[:400])
    atomic_json(output / "blind_1.json", blinded[400:])
    atomic_json(
        output / "design.json",
        {
            "version": 1,
            "cohorts": versions,
            "protocol_sha256": hashlib.sha256(
                (root / "experiments/PROTOCOL.md").read_bytes()
            ).hexdigest(),
            "primary_endpoint": "both_pass",
            "alpha": 0.05,
            "method": "SRS without replacement",
            "judge_model": "gpt-5.6-luna",
            "judge_slots_per_item": 2,
            "pilot_excluded_from_baseline": sorted(excluded),
        },
    )


if __name__ == "__main__":
    prepare(Path.cwd())
