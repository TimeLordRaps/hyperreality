"""A finite toy for "anchor preality at the big bang and at now, run it in
infinite time in finite space" (USER-STATED 2026-10-05; see PROVENANCE.md).
Ported from the Hyperstratum incubator check hm-top/preality_anchor.py.

System: Arnold's cat map on the n x n torus, (x, y) -> (2x + y, x + y) mod n.
It is a bijection, so the state space is finite and every state has exactly
one past and one future. Macrostates are b x b blocks (what an observer can
fix). The toy illustrates what "a locked landmark additional to the big bang"
can mean as a two-boundary problem. It is not evidence that any physical
system behaves this way. [FORM] for the finite computation; [HYPOTHETICAL]
as a reading of the owner's statement."""

import unittest

N, B = 60, 10
M = ((2, 1), (1, 1))
IDENT = ((1, 0), (0, 1))


def states(n=N):
    return [(x, y) for x in range(n) for y in range(n)]


def fwd(s, n=N):
    x, y = s
    return ((2 * x + y) % n, (x + y) % n)


def bwd(s, n=N):
    x, y = s
    return ((x - y) % n, (-x + 2 * y) % n)


def block(s, b=B):
    return (s[0] // b, s[1] // b)


def is_bijection(step, n=N):
    return sorted(map(step, states(n))) == sorted(states(n))


def has_exact_inverse(step, inverse, n=N):
    return all(inverse(step(s)) == s and step(inverse(s)) == s for s in states(n))


def matmul(a, b, n=N):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) % n for j in range(2))
                 for i in range(2))


def period(n=N, limit=10_000):
    """Smallest P > 0 with M^P = identity mod n; bounded by `limit`."""
    a, p = M, 1
    while a != IDENT:
        if p >= limit:
            raise ValueError("no period found within the bound")
        a, p = matmul(a, M, n), p + 1
    return p


def end_blocks(macro, steps):
    """How many microstates of `macro` land in each macrostate after `steps`."""
    counts = {}
    for s in (s for s in states() if block(s) == macro):
        t = s
        for _ in range(steps):
            t = fwd(t)
        counts[block(t)] = counts.get(block(t), 0) + 1
    return counts


class ReversibilityTests(unittest.TestCase):
    def test_cat_map_is_a_bijection_with_an_exact_inverse(self):
        self.assertEqual(len(states()), 3600)
        self.assertTrue(is_bijection(fwd))
        self.assertTrue(has_exact_inverse(fwd, bwd))

    def test_non_reversible_map_is_rejected_negative_control(self):
        def squash(s):
            x, y = s
            return ((2 * x + y) % N, (2 * x + 2 * y) % N)
        self.assertFalse(is_bijection(squash))


class FiniteLoopTests(unittest.TestCase):
    def test_period_is_sixty(self):
        self.assertEqual(period(), 60)

    def test_forward_run_repeats_exactly_after_one_period(self):
        start = (7, 13)
        t, orbit = start, {start}
        for _ in range(period()):
            t = fwd(t)
            orbit.add(t)
        self.assertEqual(t, start)
        self.assertLessEqual(len(orbit), 60)

    def test_a_longer_run_adds_no_new_states(self):
        start, t, seen = (7, 13), (7, 13), set()
        for _ in range(3 * period()):
            seen.add(t)
            t = fwd(t)
        self.assertEqual(len(seen), 60)


class PastTimelineTests(unittest.TestCase):
    macro = (2, 3)

    def test_a_macro_moment_has_one_timeline_per_compatible_microstate(self):
        micro = [s for s in states() if block(s) == self.macro]
        self.assertEqual(len(micro), 100)
        past = {s: s for s in micro}
        for _ in range(200):
            past = {s: bwd(p) for s, p in past.items()}
        self.assertEqual(len(set(past.values())), 100)

    def test_a_microstate_has_one_exact_past(self):
        s = (7, 13)
        t = s
        for _ in range(200):
            t = fwd(t)
        for _ in range(200):
            t = bwd(t)
        self.assertEqual(t, s)


class SecondAnchorTests(unittest.TestCase):
    macro = (2, 3)

    def test_second_anchor_keeps_one_to_nine_with_mean_about_two_point_eight(self):
        counts = end_blocks(self.macro, 100)
        self.assertEqual(sum(counts.values()), 100)
        possible = (N // B) ** 2
        self.assertEqual(possible, 36)
        self.assertEqual(round(100 / possible, 1), 2.8)
        self.assertEqual((min(counts.values()), max(counts.values())), (1, 9))

    def test_anchoring_never_adds_timelines_and_every_count_is_positive(self):
        counts = end_blocks(self.macro, 100)
        self.assertTrue(all(v >= 1 for v in counts.values()))
        self.assertLessEqual(len(counts), 36)

    def test_no_anchor_keeps_all_one_hundred_negative_control(self):
        # Zero steps: the "second" macro-moment is the first, all 100 stay.
        self.assertEqual(end_blocks(self.macro, 0), {self.macro: 100})


if __name__ == "__main__":
    unittest.main()
