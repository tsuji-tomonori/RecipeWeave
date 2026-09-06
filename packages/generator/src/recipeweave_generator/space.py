"""バージョン管理する有限の候補空間を、一様な通し番号抽出と逐次出力で扱う。"""

from __future__ import annotations

import bisect
import hashlib
import itertools
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def unrank(items: tuple[str, ...], k: int, rank: int) -> tuple[str, ...]:
    if k < 0 or k > len(items) or not 0 <= rank < math.comb(len(items), k):
        raise ValueError("combination rank outside its domain")
    out: list[str] = []
    start = 0
    for remaining in range(k, 0, -1):
        for index in range(start, len(items) - remaining + 1):
            size = math.comb(len(items) - index - 1, remaining - 1)
            if rank < size:
                out.append(items[index])
                start = index + 1
                break
            rank -= size
    return tuple(out)


@dataclass(frozen=True)
class Segment:
    template: int
    main: str
    supports: tuple[str, ...]
    k: int
    flavors: tuple[str, ...]
    routes: tuple[str, ...]
    choices: tuple[tuple[str, ...], ...] | None = None

    @property
    def count(self) -> int:
        size = (
            len(self.choices) if self.choices is not None else math.comb(len(self.supports), self.k)
        )
        return size * len(self.flavors) * len(self.routes)

    def point(self, ordinal: int) -> tuple[int, str, tuple[str, ...], str, str]:
        route = self.routes[ordinal % len(self.routes)]
        ordinal //= len(self.routes)
        flavor = self.flavors[ordinal % len(self.flavors)]
        ordinal //= len(self.flavors)
        aux = (
            self.choices[ordinal]
            if self.choices is not None
            else unrank(self.supports, self.k, ordinal)
        )
        return self.template, self.main, aux, flavor, route


class Space:
    def __init__(self, definition: dict[str, Any]) -> None:
        self.definition = definition
        self.digest = hashlib.sha256(canonical(definition)).hexdigest()
        self.blocks = definition["blocks"]
        self.segments: list[Segment] = []
        self.ends: list[int] = []
        self.names: dict[str, str] = {}
        codes = [b["code"] for b in self.blocks]
        if len(set(codes)) != len(codes):
            raise ValueError("duplicate template codes")
        total = 0
        for t, block in enumerate(self.blocks):
            self.names.update(block["primary"])
            self.names.update(block["supports"])
            for field in ("k", "flavors", "routes"):
                if not block[field] or len(set(block[field])) != len(block[field]):
                    raise ValueError(f"empty or duplicate {field}")
            for main in sorted(block["primary"]):
                aux = tuple(sorted(set(block["supports"]) - {main}))
                for k in sorted(block["k"]):
                    if k < 1 or k > 3:
                        raise ValueError("only 1..3 support ingredients are supported")
                    if k > len(aux):
                        continue
                    choices = None
                    if "support_sets" in block:
                        raw = [
                            tuple(sorted(x))
                            for x in block["support_sets"]
                            if len(x) == k and main not in x
                        ]
                        if len(raw) != len(set(raw)) or any(len(set(x)) != len(x) for x in raw):
                            raise ValueError("duplicate support set")
                        if any(x not in aux for choice in raw for x in choice):
                            raise ValueError("unknown support identity")
                        choices = tuple(sorted(raw))
                        if not choices:
                            continue
                    segment = Segment(
                        t, main, aux, k, tuple(block["flavors"]), tuple(block["routes"]), choices
                    )
                    total += segment.count
                    self.segments.append(segment)
                    self.ends.append(total)
        if not total or total >= 2**63:
            raise ValueError("empty or overflowing space")
        self.total = total

    @classmethod
    def load(cls, path: Path) -> Space:
        return cls(json.loads(path.read_text()))

    def point(self, ordinal: int) -> tuple[int, str, tuple[str, ...], str, str]:
        if not 0 <= ordinal < self.total:
            raise ValueError("ordinal outside space")
        i = bisect.bisect_right(self.ends, ordinal)
        return self.segments[i].point(ordinal - (self.ends[i - 1] if i else 0))

    def describe(self, ordinal: int) -> dict[str, Any]:
        t, main, aux, flavor, route = self.point(ordinal)
        return {
            "structure": self.blocks[t]["label"],
            "main": self.names[main],
            "supports": [self.names[x] for x in aux],
            "flavor": flavor,
            "route": route,
        }

    def sample(self, n: int, seed: int) -> list[int]:
        if not 0 < n <= self.total:
            raise ValueError("invalid sample size")
        return random.Random(seed).sample(range(self.total), n)

    def iter_range(self, start: int = 0, stop: int | None = None):
        stop = self.total if stop is None else stop
        if not 0 <= start <= stop <= self.total:
            raise ValueError("invalid output interval")
        offset = 0
        for segment in self.segments:
            end = offset + segment.count
            if end <= start:
                offset = end
                continue
            if offset >= stop:
                break
            # isliceが読み飛ばす範囲を1つの有限区間に限定し、候補空間の先頭から展開しない。
            choices = (
                segment.choices
                if segment.choices is not None
                else itertools.combinations(segment.supports, segment.k)
            )
            combinations = itertools.product(choices, segment.flavors, segment.routes)
            lo, hi = max(0, start - offset), min(segment.count, stop - offset)
            for n, (aux, flavor, route) in enumerate(
                itertools.islice(combinations, lo, hi), offset + lo
            ):
                yield n, (segment.template, segment.main, aux, flavor, route)
            offset = end

    def signature(self, ordinal: int) -> str:
        t, main, aux, flavor, route = self.point(ordinal)
        return hashlib.sha256(
            canonical([self.blocks[t]["code"], main, sorted(aux), flavor, route])
        ).hexdigest()
