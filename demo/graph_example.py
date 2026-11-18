"""Synthetic feature/situation incidence and Jaccard overlap demonstration.

This module intentionally contains no model inference or private research code.
"""
from __future__ import annotations

import json
from itertools import combinations
from typing import Iterable

# All examples are fictional. These tuples are not original research observations.
SYNTHETIC_OBSERVATIONS = (
    ("Display", "Positive confirmation"),
    ("Display", "Expectation mismatch"),
    ("Display", "Neutral observation"),
    ("Battery", "Expectation mismatch"),
    ("Battery", "Product failure"),
    ("Battery", "Neutral observation"),
    ("Connectivity", "Product failure"),
    ("Connectivity", "Neutral observation"),
    ("Connectivity", "Support interaction"),
    ("Delivery", "Support interaction"),
    ("Delivery", "Expectation mismatch"),
)


def situation_sets(observations: Iterable[tuple[str, str]]) -> dict[str, set[str]]:
    """Construct a binary incidence map without counting duplicate pairs twice."""
    groups: dict[str, set[str]] = {}
    for feature, situation in observations:
        if not feature.strip() or not situation.strip():
            raise ValueError("Feature families and situations must be non-empty")
        groups.setdefault(feature, set()).add(situation)
    return groups


def jaccard(left: set[str], right: set[str]) -> float:
    """Similarity between sets; 0.0 when neither set contains any items."""
    union = left | right
    return len(left & right) / len(union) if union else 0.0


def projected_edges(observations: Iterable[tuple[str, str]]) -> list[dict[str, object]]:
    """Pairwise feature-family Jaccard weights for shared situations."""
    groups = situation_sets(observations)
    rows = []
    for a, b in combinations(sorted(groups), 2):
        shared = groups[a] & groups[b]
        if shared:
            rows.append({
                "feature_a": a,
                "feature_b": b,
                "shared_situations": sorted(shared),
                "jaccard": round(jaccard(groups[a], groups[b]), 4),
            })
    return rows


if __name__ == "__main__":
    print(json.dumps({"synthetic_projection": projected_edges(SYNTHETIC_OBSERVATIONS)}, indent=2))
