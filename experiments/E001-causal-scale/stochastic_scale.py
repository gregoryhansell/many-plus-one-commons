"""Deterministic finite sweep; no sampling, network, or external dependencies."""
import itertools
import json
import math
from causal_scale import mutual_information, coarse_grain


def partitions(n):
    def grow(groups, i):
        if i == n:
            yield [g[:] for g in groups]
            return
        for j in range(len(groups)):
            groups[j].append(i)
            yield from grow(groups, i + 1)
            groups[j].pop()
        yield from grow(groups + [[i]], i + 1)
    yield from grow([], 0)


def compare(matrix, groups):
    n, k = len(matrix), len(groups)
    matched = [0.0] * n
    for group in groups:
        for i in group:
            matched[i] = 1 / (k * len(group))
    macro = mutual_information(coarse_grain(matrix, groups), [1 / k] * k)
    return macro - mutual_information(matrix, [1 / n] * n), macro - mutual_information(matrix, matched)


def main():
    groups = [p for p in partitions(4) if 1 < len(p) < 4]
    assert len(groups) == 13
    rows = []
    for noise in [0, 0.1, 0.25, 0.5, 1]:
        gains, matched = [], []
        for mapping in itertools.product(range(4), repeat=4):
            matrix = [[(1 - noise) * (j == mapping[i]) + noise / 4
                       for j in range(4)] for i in range(4)]
            for partition in groups:
                a, b = compare(matrix, partition)
                gains.append(a)
                matched.append(b)
                assert b <= 1e-12, (mapping, noise, partition, b)
        rows.append(dict(noise=noise, comparisons=len(gains),
                         uniform_positive=sum(x > 1e-12 for x in gains),
                         matched_positive=sum(x > 1e-12 for x in matched),
                         max_uniform_gain=round(max(gains), 12),
                         min_matched_gain=round(min(matched), 12),
                         max_matched_gain=round(max(matched), 12)))
    # Identity retains two bits microscopically; a balanced binary partition loses one.
    identity = [[int(i == j) for j in range(4)] for i in range(4)]
    assert math.isclose(compare(identity, [[0, 1], [2, 3]])[1], -1)
    # Original deterministic construction attains matched equality.
    original = [[1, 0, 0, 0]] * 3 + [[0, 0, 0, 1]]
    assert abs(compare(original, [[0, 1, 2], [3]])[1]) < 1e-12
    print(json.dumps(dict(experiment='E001-S', version=1,
                         scope='256 deterministic maps mixed with uniform output noise; 13 strict nontrivial partitions',
                         total_comparisons=sum(r['comparisons'] for r in rows),
                         tolerance=1e-12, results=rows, checks_passed=True), indent=2))

if __name__ == '__main__':
    main()
