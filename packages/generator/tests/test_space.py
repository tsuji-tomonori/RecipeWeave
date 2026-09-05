import csv
import gzip
import hashlib
import itertools
import json
import math
from pathlib import Path

import pytest
from recipeweave_generator.catalog import compile_catalog
from recipeweave_generator.export import export_all, file_hash, verify_all
from recipeweave_generator.space import Space, canonical, unrank


def tiny():
    return {
        "version": "test",
        "blocks": [
            {
                "code": "stir",
                "label": "炒め",
                "primary": {"a": "A", "b": "B"},
                "supports": {"a": "A", "c": "C", "d": "D"},
                "k": [1, 2],
                "flavors": ["醤油", "味噌"],
                "routes": ["炒め", "蒸す"],
            }
        ],
    }


def test_unrank_against_independent_exhaustive_enumerator():
    for n in range(1, 10):
        for k in range(min(n, 3) + 1):
            items = tuple(str(x) for x in range(n))
            expected = list(itertools.combinations(items, k))
            assert [unrank(items, k, i) for i in range(math.comb(n, k))] == expected
    with pytest.raises(ValueError):
        unrank(("a",), 1, 1)


def test_count_ordinal_range_and_signature_are_consistent():
    s = Space(tiny())
    expected = [
        (0, p, aux, f, r)
        for p in ["a", "b"]
        for k in [1, 2]
        for aux in itertools.combinations(sorted({"a", "c", "d"} - {p}), k)
        for f in ["醤油", "味噌"]
        for r in ["炒め", "蒸す"]
    ]
    assert s.total == len(expected)
    assert list(s.iter_range()) == list(enumerate(expected))
    assert [s.point(i) for i in range(s.total)] == expected
    assert len({s.signature(i) for i in range(s.total)}) == s.total
    assert list(s.iter_range(7, 25)) == list(enumerate(expected))[7:25]
    assert s.sample(10, 5) == s.sample(10, 5)
    with pytest.raises(ValueError):
        s.point(-1)
    with pytest.raises(ValueError):
        s.point(s.total)


def test_cross_role_pairs_not_arbitrary_pairs():
    d = tiny()
    d["blocks"][0]["support_sets"] = [["c"], ["a", "d"]]
    s = Space(d)
    assert all(set(p[2]) in ({"c"}, {"a", "d"}) for _, p in s.iter_range())
    assert all(s.point(n) == p for n, p in s.iter_range())
    d["blocks"][0]["support_sets"].append(["d", "a"])
    with pytest.raises(ValueError):
        Space(d)


def test_export_resume_and_corruption_detection(tmp_path):
    s = Space(tiny())
    m = export_all(s, tmp_path, 7)
    assert m["status"] == "complete"
    assert verify_all(tmp_path)["rows_verified"] == s.total
    assert export_all(s, tmp_path, 7) == m
    # A interrupted run retains only finalized shard entries.
    manifest_path = tmp_path / "manifest.json"
    interrupted = json.loads(manifest_path.read_text())
    interrupted["shards"] = interrupted["shards"][:1]
    interrupted["status"] = "incomplete"
    manifest_path.write_text(json.dumps(interrupted))
    assert export_all(s, tmp_path, 7) == m
    part = tmp_path / m["shards"][0]["file"]
    part.write_bytes(b"corrupt")
    with pytest.raises(ValueError):
        export_all(s, tmp_path, 7)


@pytest.mark.parametrize("damage", ["duplicate", "missing", "order", "filename", "columns"])
def test_damaged_manifest_is_rejected_without_rewriting(tmp_path, damage):
    s = Space(tiny())
    manifest = export_all(s, tmp_path, 7)
    if damage == "duplicate":
        manifest["shards"].append(manifest["shards"][0])
    elif damage == "missing":
        manifest["shards"].pop()
    elif damage == "order":
        manifest["shards"].reverse()
    elif damage == "filename":
        manifest["shards"][0]["file"] = "wrong.csv.gz"
    else:
        manifest["columns"][2] = "wrong"
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest))
    before = path.read_bytes()
    with pytest.raises(ValueError):
        export_all(s, tmp_path, 7)
    assert path.read_bytes() == before
    with pytest.raises(ValueError):
        verify_all(tmp_path, s)


def test_resume_preserves_corrupt_dictionary_for_recovery(tmp_path):
    s = Space(tiny())
    export_all(s, tmp_path, 7)
    path = tmp_path / "dictionary.json"
    path.write_text('{}\n')
    with pytest.raises(ValueError, match="dictionary corruption"):
        export_all(s, tmp_path, 7)
    assert path.read_text() == '{}\n'


def test_full_verification_rejects_checksum_consistent_wrong_candidate(tmp_path):
    s = Space(tiny())
    manifest = export_all(s, tmp_path, 7)
    assert verify_all(tmp_path, s, full=True)["decoded_points_matched"] == s.total
    with pytest.raises(ValueError, match="requires a definition"):
        verify_all(tmp_path, full=True)
    path = tmp_path / manifest["shards"][0]["file"]
    with gzip.open(path, "rt", newline="") as stream:
        rows = list(csv.reader(stream))
    # Keep an existing route ID and valid ordinal; checksums alone cannot detect this.
    rows[1][7] = str(1 - int(rows[1][7]))
    with gzip.open(path, "wt", newline="") as stream:
        csv.writer(stream, lineterminator="\n").writerows(rows)
    manifest["shards"][0].update(sha256=file_hash(path), bytes=path.stat().st_size)
    (tmp_path / "manifest.json").write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="differs from ordinal definition"):
        verify_all(tmp_path, s, full=True)


def test_verification_binds_dictionary_labels_to_definition(tmp_path):
    s = Space(tiny())
    manifest = export_all(s, tmp_path, 7)
    path = tmp_path / "dictionary.json"
    dictionary = json.loads(path.read_text())
    dictionary["templates"][0]["name"] = "別の料理"
    path.write_text(json.dumps(dictionary))
    manifest["dictionary_sha256"] = hashlib.sha256(canonical(dictionary)).hexdigest()
    (tmp_path / "manifest.json").write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="dictionary does not match definition"):
        verify_all(tmp_path, s, full=True)


def test_concentration_variants_do_not_multiply_candidates():
    root = Path(__file__).resolve().parents[3]
    src = json.loads((root / "data/catalog/source_foods.json").read_text())
    policy = json.loads((root / "data/catalog/policy.json").read_text())
    definition, report = compile_catalog(src, policy)
    tsuyu = [v for v in report["variants"] if v["name"].startswith("めんつゆ")]
    assert {x["concentration_multiplier"] for x in tsuyu} == {2, 3, 4}
    assert len({v["identity_id"] for v in tsuyu}) == 1
    assert all(v["conversion_reference"] is None for v in tsuyu)
    assert all(
        not any("めんつゆ2倍" in str(x) or "めんつゆ3倍" in str(x) for x in b["flavors"])
        for b in definition["blocks"]
    )
    assert report["source_foods"] == 1005
