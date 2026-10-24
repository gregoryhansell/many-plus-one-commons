# E001: When the scale changes, check the interventions

**Status:** executed, reproducible toy calculation. **Date:** 2026-10-23.  
**Scope:** an original mathematical illustration, not a new empirical discovery, a replication of an entire paper, or a consciousness test.

## Question

Can a macro model convey more information about its next state than a micro model, and what exactly changed in the comparison?

Consider four microstates. States 0, 1, and 2 transition deterministically to state 0. State 3 transitions to itself. Group the first three as macrostate A and the last as macrostate B. At the macro level, A leads to A and B leads to B.

Calculate mutual information between the intervention state X and the next state Y:

`I(X;Y) = sum_x,y p(x) p(y|do(x)) log2[p(y|do(x)) / p(y)]`.

For uniform interventions at each respective scale, this is an effective-information comparison. The implementation accepts an explicit intervention distribution so the change in that distribution is visible.

## Executed result

| Comparison | Information, bits |
| --- | ---: |
| Micro model, uniform across four microstates | 0.811278124459 |
| Macro model, uniform across two macrostates | 1.000000000000 |
| Difference under the two uniform conventions | 0.188721875541 |
| Micro model, distribution matched to uniform macro interventions | 1.000000000000 |
| Macro model, distribution induced by uniform micro interventions | 0.811278124459 |
| Macro advantage with the matched intervention distribution | 0.000000000000 |

The first comparison really does favor the macro model under the chosen convention. But uniformity at the two scales means different interventions: uniform micro inputs give A probability 3/4, while uniform macro inputs give A probability 1/2. Redistributing micro input probabilities to `(1/6, 1/6, 1/6, 1/2)` reproduces the macro result. The advantage disappears when this intervention change is controlled in this particular example.

## What the example teaches

Coarse-graining and intervention choice must be reported together. The result does not refute causal-emergence research: choosing useful interventions can itself be part of the question, and other models require their own analysis. Nor does the initial advantage establish irreducible new powers. It identifies an exact dependency that an overly quick metaphysical interpretation could conceal.

This tightens C002: before treating a numerical macro advantage as evidence for a stronger emergence claim, compare intervention distributions, accessible manipulations, and state partitions. Ask whether the macro interventions are physically meaningful for the actual system, not merely mathematically convenient.

The broader inspiration is Hoel's [When the Map Is Better Than the Territory](https://arxiv.org/abs/1612.09592), whose abstract and bibliographic record were consulted. The four-state construction, control comparison, and code here are this project's own pedagogical development. They do not claim to reproduce Hoel's full derivation or establish novelty in the literature.

## Reproduce

From the repository root:

```bash
python3 experiments/E001-causal-scale/causal_scale.py
```

The script uses only Python's standard library. It validates probability distributions, checks a perfect and a noisy binary channel, verifies the coarse-graining, and compares results with analytic entropy. [results.json](results.json) contains the recorded output. No private data, randomness, model calls, credentials, or network access are used.

## Strongest objection and next test

The example is deliberately simple and deterministic. Its disappearance of the advantage is not a theorem about every coarse-graining, and it says nothing directly about biological individuality. A useful next contribution should introduce stochastic transitions, alternative partitions, and constraints on allowed interventions; report which comparisons retain an advantage and why.

[P002](../../papers/P002-relational-individuality.md) · [C002](../../claims/C002-novelty-and-emergence.md) · [Atlas](../../atlas/Home.md)
