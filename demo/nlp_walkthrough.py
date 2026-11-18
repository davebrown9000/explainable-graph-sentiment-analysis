"""Independent, fictional feature-to-situation walkthrough.

Illustrative string rules only: NOT PyABSA, spaCy, VADER or research code.
No model inference, ground-truth evaluation or causal attribution is performed.
"""
from __future__ import annotations

import json
import re

from demo.graph_example import projected_edges

# Fictional mini-corpus; not sampled from the dissertation dataset.
REVIEWS = (
    ("R01", "The camera is excellent but the battery fails."),
    ("R02", "The battery works well but the display is broken."),
    ("R03", "The camera works well and the display is excellent."),
    ("R04", "The battery fails but the camera is excellent."),
    ("R05", "Shipping was late."),
)

# Synthetic categories are intentionally small; these are not the full
# governed feature taxonomy or customer-situation rules from the research.
ALIASES = {"camera": "Camera", "battery": "Battery", "display": "Display"}
CUES = (
    ("fails", "Product failure", "negative"),
    ("broken", "Product failure", "negative"),
    ("excellent", "Positive confirmation", "positive"),
    ("works well", "Positive confirmation", "positive"),
)


def clauses(text: str) -> list[str]:
    """Split only on a toy contrast marker, preserving clause order."""
    if not isinstance(text, str):
        raise TypeError("review must be text")
    return [part.strip(" .!") for part in re.split(r"\s+but\s+", text, flags=re.I) if part.strip(" .!")]


def feature_rows(review_id: str, text: str) -> list[dict[str, object]]:
    """Emit traceable heuristic rows; no aspect model is used.

    Multiple feature mentions in a clause share a cue. This is a known
    limitation and is deliberately visible rather than disguised as ABSA.
    """
    if not isinstance(review_id, str) or not review_id.strip():
        raise ValueError("review_id must be non-empty")
    result = []
    for clause_index, clause in enumerate(clauses(text), start=1):
        found = sorted(
            {family for alias, family in ALIASES.items()
             if re.search(r"\b" + re.escape(alias) + r"\b", clause, flags=re.I)}
        )
        if not found:
            continue
        matched = next(((cue, situation, polarity) for cue, situation, polarity in CUES
                        if re.search(r"\b" + re.escape(cue) + r"\b", clause, flags=re.I)), None)
        for family in found:
            result.append({
                "review_id": review_id,
                "clause_index": clause_index,
                "feature_family": family,
                "rationale": clause,
                "cue": matched[0] if matched else None,
                "situation": matched[1] if matched else "Unclassified",
                "heuristic_polarity": matched[2] if matched else "unknown",
            })
    return result


def analyse(reviews: tuple[tuple[str, str], ...] = REVIEWS) -> dict[str, object]:
    """Return transparent rows and a Jaccard projection of classified pairs."""
    ids = [review_id for review_id, _ in reviews]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate review_id")
    rows = [row for review_id, text in reviews for row in feature_rows(review_id, text)]
    links = [(str(row["feature_family"]), str(row["situation"]))
             for row in rows if row["situation"] != "Unclassified"]
    return {
        "kind": "fictional_heuristic_walkthrough",
        "review_count": len(reviews),
        "feature_rows": rows,
        "jaccard_projection": projected_edges(links),
    }


if __name__ == "__main__":
    print(json.dumps(analyse(), indent=2))
