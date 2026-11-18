# Research methodology — from NLP to interpretable networks

This account describes the **completed private academic workflow**, reconciled against the dissertation report, original artefact records, viva presentation and earlier reconstructed research repository. It is a methodological explanation, **not** an executable specification or a release of the original code.

## 1. Corpus preparation and sentence segmentation

The source corpus contained **3,062 customer reviews** of iPhone 13, 14 and 15 products. Review text and product/variant metadata were normalised while preserving device terminology, chip identifiers, quantities and other relevant technical expressions. Manually curated identifier mappings were used to align product and variant metadata; ambiguous cross-mappings were audited.

The study used **spaCy sentence segmentation with additional boundary logic**, handling periods, ellipses, exclamation marks and percentage markers while avoiding undesirable breaks in abbreviations and numeric expressions. A minimum-length constraint reduced fragmentary units. This yielded **11,534 sentences**.

A stable **`review_id`** identified the source review, with **`sent_id`** maintaining traceability at sentence level. Later processing also required **feature-level rows**, since a sentence may discuss more than one product aspect. The conceptual grain is:

```text
review_id  ->  sent_id  ->  (sentence, identified feature)  ->  sentiment / situation
```

The distinction matters: a sentence-level VADER label cannot automatically substitute for one or several feature-specific ABSA labels. Composite or review-scoped identifiers, rather than an unqualified sentence ordinal, protect joins across reviews. The report documents semantic identifiers and strict merge checks; exact private encoding conventions are intentionally not reproduced here.

## 2. NLP feature discovery and taxonomy governance

Feature identification was a **hybrid extraction and curation** stage, not simply a list of keywords.

- **Named Entity Recognition:** spaCy proposed candidate entities with initial `ORG`, `PRODUCT` and `GPE` types. Outputs were reviewed and canonicalised into a project-specific entity scheme (`PRO`, `ORG`, `GPE`, `NOISE`). Common device-expression errors, including storage capacity, chipset and operating-system references, were corrected through dictionaries, pattern rules and manual review.
- **Recall improvement:** corrected entity counts supported a curated matching pass with priority ordering (organisation, product, location) and regular expressions for device-specific expressions. The resulting entities were deduplicated before merging into the sentence records.
- **Aspect extraction:** spaCy noun chunks supplied candidates. Stop/drop lists, disambiguation rules and frequency tiers distinguished meaningful aspects from noise. Contextual binding prevented broad nouns such as “quality” or “health” being treated as specific features without an appropriate local anchor.
- **Unified feature mentions:** governed aspect candidates were combined with an allowed subset of product entities, normalised and subjected to targeted rewrites. A single coarse fallback feature was assigned only where extraction yielded no qualifying aspect.
- **Feature families:** individual features were mapped deterministically into broader analytical families to reduce sparsity and support interpretable graph aggregation.

This stage generated **13,102 sentence–feature records**, representing **149 features across 16 families**. Research curation reported approximately **46.13%** governed aspect extraction and **53.87%** rule fallback. The fallback contribution is a material source of potential representation bias and a reason not to claim the taxonomy is fully learned or automatic.

## 3. Sentiment: sentence baseline versus feature-targeted PyABSA

### VADER baseline

VADER assigned **negative/neutral/positive/compound scores** to each sentence. Its role was a sentence-level reference for comparison, not a ground-truth label.

### PyABSA aspect-polarity inference

The private workflow used a **pretrained PyABSA Aspect Polarity Classification (APC) English checkpoint** to estimate sentiment about a **specific identified feature** rather than the sentence as a whole. The reported implementation adapted the *input context* and *target aspect*:

1. Begin with a governed **(sentence, feature)** pair.
2. Split, when applicable, around contrastive cues such as **“but”** and **“however”**, and select the clause most likely to contain the intended feature. Feature aliases were also considered for clause selection.
3. Present the feature explicitly using aspect markers, documented in the report as **`[B-ASP]` ... `[E-ASP]`**, to identify the target for prediction.
4. Run inference with the stable pretrained checkpoint; retain **polarity label, confidence and class-probability vector**.
5. Limit redundant processing through deduplication of sentence–feature inputs and a **top-*k* cap** on inferred features per sentence.
6. Rejoin the predictions to the governed feature records using canonicalised keys, strict one-to-one validation and row-count checks.

**Precision about the “nearby words” mechanism:** The dissertation describes *contrast-aware clause selection and explicit aspect marking* to focus the input before PyABSA inference. It does **not** establish that the PyABSA model itself was retrained with a custom fixed-distance attention window or that its internal attention was altered. A separate **bounded token/dependency context window** was used in the next stage for situation attribution.

The study did **not** train or fine-tune new PyABSA model weights. Its research emphasis was the interpretability of sentiment combined with contextual and relational analysis, not classifier benchmarking.

## 4. Feature-centred contextual situation attribution

A feature-level sentiment label indicates *what* was judged favourably or unfavourably; it does not inherently explain the customer circumstances associated with that judgement.

The situation stage derived **rationale spans** around feature mentions. spaCy was used, where possible, to locate the feature's syntactic head. Bounded context was assembled using both a fixed token window and a constrained dependency subtree, capped to avoid overly broad evidence spans. The system computed multi-hot lexical/dependency cues including:

- negation and modality;
- requirement or purchase-necessity language;
- missingness or absence;
- breakdown, intermittent failure and damage;
- comparisons, expectations, and positive/neutral confirmation cues.

An ordered and auditable **rule system** combined these cues, aspect polarity and domain lexicons to assign situations such as `PRODUCT_FAILURE`, `EXPECTATION_MISMATCH`, `COMPETITOR_COMPARISON`, `POSITIVE_CONFIRMATION` and physical-condition/absence scenarios. The implementation also distinguished certain comparison types and arrival damage from later wear. A rule-strength **assignment confidence** was retained; it is **not a calibrated probability that the inferred cause is true**.

Situation labels were mapped to a **domain bucket → sub-domain → topic** hierarchy. A priority rule provided a primary sentence situation when multiple feature-level situations were present, with multi-topic flags retained. Generic `overall` rows were excluded from the primary network-ready subset. Of the **6,675** retained feature–situation rows, **3,008** had `UNCLASSIFIED_CAUSE`: the method deliberately preserved uncertainty instead of forcing a causal story for every observation.

## 5. Bipartite network construction

The model aggregated annotated feature-level observations by **(feature family, situation)**, producing a graph with two distinct node types:

```text
Feature family (partition A)  <-- weighted evidence -->  Situation (partition B)
```

An edge indicated observed co-occurrence under the situation-attribution rules. Its attributes included:

- observation frequency;
- positive, neutral and negative ABSA counts;
- a signed sentiment aggregate (`+1`, `0`, `−1` mapping);
- mean ABSA and situation-assignment confidence;
- prevalence of negation, modality, failure, absence and requirement cues.

The primary research graph contained **15 feature-family nodes**, **15 situation nodes** and **140 weighted edges**. Edges do not demonstrate a real-world causal mechanism: they describe relationships in the study's annotated and governed corpus.

## 6. Projection and community detection

To compare feature families, their **shared situation neighbours** were examined. The research considered a straightforward shared-neighbour projection, an intensity-weighted co-occurrence projection and **Jaccard similarity**:

\[
J(F_i,F_j)=\frac{|N(F_i)\cap N(F_j)|}{|N(F_i)\cup N(F_j)|}
\]

Here, `N(F)` denotes the set of *attributed situation labels* connected to feature family `F`, **not** the set of similar words or reviews. A top-*k* nearest-neighbour filter reduced an otherwise dense projection. **Louvain community detection** then identified groups with similar attributed situations.

The final filtered feature-family projection contained **15 nodes, 45 edges and three Louvain communities**. Weighted strength and betweenness supported interpretation. The network was also diagnostic: disproportionate prominence of broad fallback families prompted upstream taxonomy revisions rather than blind acceptance of network output. Network files were examined visually using NetworkX/Gephi workflows.

## 7. Association-rule mining and triangulation

The original analysis used Apriori-style association-rule mining over **sentence-scoped transactions** containing namespaced feature-family and situation items. Sentence identity must be scoped to its source review to prevent unrelated reviews being merged. This is an important documented engineering lesson in the later reconstruction.

Rules were summarised by **support, confidence and lift**. Unlike an undirected graph edge, a rule's confidence depends on the chosen antecedent and consequent. Reciprocal rules may have the same lift but different confidence.

The rules were used primarily to **sense-check and contextualise** graph structure. Some high-lift results reflected annotation conventions or platform context rather than independent behavioural discoveries; they were treated as diagnostics. Neither an association rule nor a shared-situation network edge establishes causality.

## 8. Comparative analysis and limitations

Model- and condition-specific subgraphs and sentiment profiles were examined for additional context. Their interpretability depends on support thresholds and consistent definitions of feature families and situations. The main study was descriptive rather than formally hypothesis-testing generalisable effects.

**Limitations:** one source and product family; pretrained sentiment-model errors; research-governed taxonomy and fallback decisions; unclassified situations; token/lexicon rule dependence; threshold sensitivity; no temporal diffusion analysis; no causal identification; and no independently reproduced numerical results in this public repository.

## Public demonstration boundary

The accompanying `demo/graph_example.py` is a **new fictional Jaccard illustration**, not this end-to-end methodology. It has no spaCy, VADER or PyABSA inference, situation-rule engine, weighted full research graph, Louvain optimisation or association mining. It cannot regenerate the reported results. Original source reviews, research notebooks, corrections, model assets and private source code remain outside the public repository.
