# Fictional NLP-to-graph walkthrough

This **independently authored teaching example** extends the existing binary-Jaccard graph demonstration with a visible path from invented product-review text to labelled feature–situation pairs.

## Procedure

1. Keep an explicit review ID and split text into clauses at the toy contrast marker `but`.
2. Match three fictional feature aliases using case-insensitive word boundaries.
3. Assign a clause-level cue and polarity using a deliberately small, ordered rule table.
4. Preserve the rationale text, cue, clause index and assigned situation with each feature row.
5. Use classified feature–situation pairs to construct a binary incidence projection with the separately implemented Jaccard function.

The example intentionally keeps unknown situations unclassified and reviews without matching features out of the feature table.

## Run

Python 3.11+, standard library:

```bash
python3 -m demo.nlp_walkthrough
python3 -m unittest discover -s tests -v
```

## Critical differences from the original research

| Public walkthrough | Original MSc methodology |
|---|---|
| Literal split around the word `but` | spaCy segmentation plus governed clause/context selection |
| Three exact feature aliases | Governed taxonomy and feature extraction with manual corrections |
| Fixed keyword cue and heuristic polarity | Pretrained PyABSA aspect-level inference plus rule-based contextual situation attribution |
| Binary situation incidence and Jaccard | Weighted bipartite networks, community detection, richer metrics and association rules |
| Five invented reviews | The separate, private full academic dataset and implementation |

**Do not interpret the heuristic polarity as model output.** A clause with more than one feature receives the same cue for each feature; negation, sarcasm, idioms and long-range dependencies are not understood. Jaccard measures overlap among assigned labels, not causal explanation. The example does not reproduce published research results.

## Data protection

All sentences, aliases and code in this module are new and fictional. No original customer reviews, notebooks, model assets or private project implementation are distributed.
