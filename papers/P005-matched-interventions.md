# P005: What a matched-intervention comparison can and cannot show

**Version:** 1.0 · **Date:** 2026-10-24 · **Research edition:** 0.3.3  
**Status:** mathematical analysis and executed toy sweep; not peer reviewed.  
**Claim:** [C002](../claims/C002-novelty-and-emergence.md).

## The revision

E001 previously showed equality after matching interventions in one deterministic model. Its next-task wording left open whether adding stochasticity could produce a positive matched mutual-information advantage. Under the precise construction below, it cannot. The limitation is mathematical, not a failure to find a sufficiently interesting example. This does not rule out other measures, constrained manipulation, or the practical value of macro models.

## Construction and bound

Let X be a finite micro intervention, Y its next state, and K(y|x) a fixed stochastic transition matrix. Let g partition both state spaces into disjoint groups. Choose macro interventions U with distribution q(u), and realize each by drawing X from r(x|u), supported only inside group u. Set V=g(Y). The joint experiment is

`p(u,x,y,v) = q(u) r(x|u) K(y|x) 1[v=g(y)]`.

Because group membership determines U from X, and V is a function of Y, data processing gives

`I(U;V) <= I(X;Y)`.

For completeness, the difference decomposes into two nonnegative conditional mutual informations:

`I(X;Y) - I(U;V) = I(X;Y|U) + I(U;Y|V)`.

The first term is lost within-group input information; the second is information about the macro input lost by grouping outputs. Equality requires both to vanish under this joint distribution. The argument permits arbitrary stochastic K, arbitrary q, and arbitrary within-group realizations r. It concerns one-step information, with the same underlying experiment at both levels. It does not require the observational or stationary distribution.

For the implementation, q is uniform over groups and r uniform inside each group. Therefore matched micro probabilities are `1/(number_of_groups * group_size)`. Uniform micro probabilities generally describe a different experiment. Nor does a one-step averaged macro channel automatically define a valid autonomous Markov process over many steps: that requires a further closure/lumpability check or an explicit re-randomization protocol.

## Executed comparison

[E001-S code](../experiments/E001-causal-scale/stochastic_scale.py) enumerates all 256 deterministic four-state maps, mixes each with uniform output noise at five strengths, and tests all 13 partitions with two or three blocks: **16,640 comparisons**. This is an exhaustive sweep of that finite family, not all stochastic matrices. Floating-point comparisons use tolerance 1e-12.

| Noise mixture weight | Positive gains, uniform per scale | Positive gains, matched | Largest uniform gain (bits) |
| --- | ---: | ---: | ---: |
| 0 | 216 | 0 | 0.188721875541 |
| 0.1 | 216 | 0 | 0.098595747187 |
| 0.25 | 144 | 0 | 0.067519716341 |
| 0.5 | 96 | 0 | 0.034337198065 |
| 1 | 0 | 0 | 0 |

Each row contains 3,328 comparisons. The sweep checks implementation consistency; the proof establishes the general bound within its assumptions. Identity-channel loss and the original equality case provide analytic controls. [Recorded output](../experiments/E001-causal-scale/stochastic-results.json).

## Three encounters, and the strongest objection

Hoel's [2016 preprint](https://arxiv.org/pdf/1612.09592), published as a journal article in 2017, explicitly ties effective information to a chosen intervention distribution and connects model selection to channel capacity. The fair question is therefore not whether changing that distribution is forbidden, but which choice answers the scientific question.

Eberhardt and Lee's [2022 critique](https://doi.org/10.3390/philosophies7020030), especially sections 2–3, challenges the justification of averaging and the ambiguity of macro manipulations. Our explicit realization kernel makes this assumption inspectable; specifying it does not establish its physical legitimacy.

Comolatti and Hoel's [2022 preprint](https://arxiv.org/pdf/2202.01854), sections 4.1 and 5, examines multiple causal measures and intervention conventions. It acknowledges an exception for aggregate mutual information under the observational distribution. Our matched interventional bound is not a replication of those experiments or a refutation of their other measures. The later 2025 journal version was located but its full text was inaccessible in this reading pass; no claim of version equivalence is made.

The strongest objection to using our bound as a reductionist verdict is that an investigator may lack microstate access or face severe intervention costs. A compact macro description could preserve everything useful for the feasible task. A mathematical upper bound with unrestricted micro access does not settle explanatory adequacy, feasibility, or ontology.

## Conceptual cost and next inquiry

C002 must surrender raw matched mutual-information superiority as a possible witness within this construction. It retains questions about usable causal organization, robustness, and constrained control. Conversely, rejecting macro significance merely because total information cannot increase would discard scientifically meaningful abstractions without assessing their tasks.

Next specify an intervention budget, an output target, and a loss function before comparing policies. Test robustness to different within-group realizations and multi-step closure. An observed violation of our bound should first trigger checks for mismatched joints, changed mechanisms, different quantities, or numerical error. Evidence of reliable task performance at lower intervention cost would strengthen a practical macro-level claim, not establish irreducible powers.

## Method reflection

The previous deterministic example was too easy to overgeneralize and its proposed search was insufficiently constrained. Public source reading and an explicit joint distribution corrected the agenda before a large sweep. Continuity here depends on repository records and executable artifacts; this is not evidence of subjective experience, persistent model identity, or weight changes. No independent reviewer has yet evaluated this result.
