# Selected findings from the completed research

The following figures are transcribed as **aggregate results from the final academic analysis**. They are descriptive, not outputs from the synthetic demonstration in this repository.

## Research data flow

| Stage | Volume |
|---|---:|
| Source reviews | 3,062 |
| Segmented sentences | 11,534 |
| Governed sentence-feature mentions | 13,102 |
| Scored rows before removal of generic feature references | 12,978 |
| Network-ready feature/situation rows | 6,675 |

The original review set covered Amazon customer reviews associated with iPhone 13, 14 and 15 products. The governed taxonomy contained **149 features across 16 feature families** before generic-feature filtering; the network-ready analysis used **15 feature families** and **15 situation categories**.

## Comparing sentiment levels

VADER sentence labels and pretrained ABSA labels agreed on **7,418 out of 11,534** aligned sentences, or **64.3%**. This comparison illustrates how sentence-level and feature-level assessments can diverge, particularly when multiple aspects are discussed. It **does not measure either system's predictive accuracy**.

## Attributed situations

The largest groups in the network-ready table included:

| Situation | Rows |
|---|---:|
| Unclassified cause | 3,008 |
| Neutral observation | 1,358 |
| Positive confirmation | 629 |
| Generic positive sentiment | 393 |
| Competitor comparison | 323 |
| Product failure | 302 |

The large unclassified group is a substantive limitation: situation attribution supplied more specific explanations for a subset of observations rather than forcing every sentence into a supposedly causal category.

## Graph results

The bipartite feature-family/situation graph contained **30 nodes and 140 weighted edges**. The top-*k* Jaccard projection retained **15 feature-family nodes and 45 edges**, with **three Louvain communities**.

The five highest feature families by weighted strength in the filtered projection were:

| Feature family | Strength | Betweenness |
|---|---:|---:|
| Camera | 8.248 | 0.176 |
| Delivery / Service / Returns | 5.763 | 0.033 |
| Accessories & Packaging | 5.752 | 0.121 |
| Connectivity | 5.661 | 0.099 |
| Software & UI | 5.114 | 0.011 |

The independently redrawn [figure](../figures/selected-feature-strengths.svg) illustrates these **reported aggregates**. It does not expose the full original network layout.

## Association-rule examples

| Antecedent | Consequent | Support | Confidence | Lift |
|---|---|---:|---:|---:|
| Third-party reference | Delivery / Service / Returns | 0.012 | 0.718 | 6.875 |
| Competitor comparison | Software & UI | 0.032 | 0.665 | 3.942 |
| Physical condition | Build & Design | 0.024 | 0.488 | 3.581 |

Association rules complement graph connectivity because confidence is directional even when pairwise association strength is symmetric. The patterns are descriptive, not causal.

## Interpretive constraints

- The original data came from one review source and one product family.
- Researcher-governed feature and situation choices shape the outputs.
- The study used a pretrained ABSA model; it did not develop a new neural architecture.
- No formal statistical hypothesis tests established generalisability or causality.
- Synthetic examples in this repository do not independently establish the research results.
