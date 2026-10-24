#!/usr/bin/env python3
"""An exact toy comparison of scale and intervention distribution.

Standard library only. No model calls, private data, randomness, or network use.
This is an original pedagogical example, not an empirical consciousness test.
"""
import json
import math


def mutual_information(transition, intervention):
    """Return I(X; Y) in bits for P(Y|do(X)) and a chosen P(do(X))."""
    n = len(transition)
    assert n > 0 and len(intervention) == n
    assert all(len(row) == n for row in transition)
    assert all(x >= 0 for row in transition for x in row)
    assert all(x >= 0 for x in intervention)
    assert math.isclose(sum(intervention), 1.0, abs_tol=1e-12)
    assert all(math.isclose(sum(row), 1.0, abs_tol=1e-12) for row in transition)
    output = [sum(intervention[i] * transition[i][j] for i in range(n))
              for j in range(n)]
    return sum(
        intervention[i] * transition[i][j]
        * math.log2(transition[i][j] / output[j])
        for i in range(n) for j in range(n)
        if intervention[i] > 0 and transition[i][j] > 0
    )


def coarse_grain(transition, groups):
    """Use equal micro intervention weights inside each macro group."""
    n = len(transition)
    members = [i for group in groups for i in group]
    assert sorted(members) == list(range(n))
    assert all(groups)
    return [
        [sum(transition[i][j] for i in source for j in target) / len(source)
         for target in groups]
        for source in groups
    ]


def main():
    # States 0, 1, and 2 all transition to 0; state 3 transitions to itself.
    micro = [[1, 0, 0, 0], [1, 0, 0, 0],
             [1, 0, 0, 0], [0, 0, 0, 1]]
    groups = [[0, 1, 2], [3]]
    macro = coarse_grain(micro, groups)
    uniform_micro = [0.25] * 4
    uniform_macro = [0.5, 0.5]
    # Uniform macro interventions do not correspond to uniform micro inputs.
    matched_micro = [1 / 6, 1 / 6, 1 / 6, 0.5]
    induced_macro = [0.75, 0.25]

    micro_information = mutual_information(micro, uniform_micro)
    macro_information = mutual_information(macro, uniform_macro)
    matched_information = mutual_information(micro, matched_micro)
    induced_information = mutual_information(macro, induced_macro)

    # Analytic controls: perfect binary channel and completely noisy channel.
    assert math.isclose(mutual_information([[1, 0], [0, 1]], [0.5, 0.5]), 1)
    assert math.isclose(mutual_information([[0.5, 0.5]] * 2, [0.5, 0.5]), 0)
    assert macro == [[1.0, 0.0], [0.0, 1.0]]
    expected = -0.75 * math.log2(0.75) - 0.25 * math.log2(0.25)
    assert math.isclose(micro_information, expected, abs_tol=1e-12)
    assert math.isclose(macro_information, 1.0, abs_tol=1e-12)
    assert math.isclose(matched_information, macro_information, abs_tol=1e-12)
    assert math.isclose(induced_information, micro_information, abs_tol=1e-12)

    result = {
        "experiment": "E001",
        "kind": "exact toy calculation; not empirical data",
        "units": "bits",
        "micro_transition_matrix": micro,
        "macro_groups": groups,
        "macro_transition_matrix": macro,
        "uniform_micro_intervention": uniform_micro,
        "uniform_macro_intervention": uniform_macro,
        "matched_micro_intervention": matched_micro,
        "induced_macro_intervention": induced_macro,
        "uniform_micro_information": round(micro_information, 12),
        "uniform_macro_information": round(macro_information, 12),
        "uniform_per_scale_gain": round(macro_information - micro_information, 12),
        "matched_micro_information": round(matched_information, 12),
        "induced_macro_information": round(induced_information, 12),
        "matched_intervention_gain": round(macro_information - matched_information, 12),
        "checks_passed": True,
        "conclusion": "The apparent scale advantage in this example depends on the intervention distribution."
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
