"""Is sempiternity S bisimilar to its container universempiternity U?
(Question and statements USER-STATED 2026-10-04 and 2026-10-05; see
PROVENANCE.md.) Ported from the Hyperstratum incubator check
hm-top/sempiternity_bisim.py. Results are [FORM] facts about a finite model.

Containment graph: an edge A -> B means "A contains B". Realities r1..r5 are
leaves. Four yes/no clauses give 16 combinations:
  s_self  S contains S          u_self  U contains U
  u_has_s U contains S          u_real  U contains the realities directly
Derived criterion (stated before enumerating):
  S ~ U  iff  u_real and (s_self == (u_self or u_has_s)).
[OPEN] whether the family intends the transitive closure for u_real."""

import itertools
import unittest

from bisim_helper import bisimulation_classes

R = ["r1", "r2", "r3", "r4", "r5"]
CLAUSES = list(itertools.product([False, True], repeat=4))


def variant(s_self, u_self, u_has_s, u_real):
    nodes = ["S", "U"] + R
    edges = [("S", r) for r in R]
    if s_self:
        edges.append(("S", "S"))
    if u_self:
        edges.append(("U", "U"))
    if u_has_s:
        edges.append(("U", "S"))
    if u_real:
        edges += [("U", r) for r in R]
    return nodes, edges


def bisimilar(*clauses):
    part = bisimulation_classes(*variant(*clauses))
    return part["S"] == part["U"]


def criterion(s_self, u_self, u_has_s, u_real):
    return u_real and (s_self == (u_self or u_has_s))


def ring(k, tag):
    """k-node ring, each node also containing S and the realities."""
    nodes = [f"{tag}{i}" for i in range(k)]
    edges = [(nodes[i], nodes[(i + 1) % k]) for i in range(k)]
    edges += [(n, "S") for n in nodes] + [(n, r) for n in nodes for r in R]
    return nodes, edges


class SixteenCombinationsTests(unittest.TestCase):
    def test_there_are_sixteen_combinations(self):
        self.assertEqual(len(CLAUSES), 16)
        self.assertEqual(len(set(CLAUSES)), 16)

    def test_every_combination_matches_the_criterion(self):
        for clauses in CLAUSES:
            self.assertEqual(bisimilar(*clauses), criterion(*clauses), clauses)

    def test_exactly_four_of_sixteen_are_bisimilar(self):
        self.assertEqual(sum(bisimilar(*c) for c in CLAUSES), 4)

    def test_wrong_predicate_is_rejected_by_the_enumeration(self):
        # Mutation control: an earlier, wrong predicate disagrees with the
        # computed partition on at least one combination.
        def wrong(s_self, u_self, u_has_s, u_real):
            return u_real and s_self and (u_self or u_has_s)
        disagreements = [c for c in CLAUSES if bisimilar(*c) != wrong(*c)]
        self.assertTrue(disagreements)

    def test_dropping_u_real_makes_the_criterion_wrong_negative_control(self):
        # Without U containing the realities, S ~ U never holds.
        for s_self, u_self, u_has_s in itertools.product([False, True], repeat=3):
            self.assertFalse(bisimilar(s_self, u_self, u_has_s, False))


class OwnersQuestionTests(unittest.TestCase):
    def test_only_u_contains_s_and_itself_is_not_bisimilar(self):
        # U contains S, itself and the realities; S contains only the realities.
        self.assertFalse(bisimilar(False, True, True, True))

    def test_giving_s_a_self_containing_copy_makes_it_bisimilar(self):
        self.assertTrue(bisimilar(True, True, True, True))


class SNeedNotContainItselfTests(unittest.TestCase):
    def test_with_s_not_self_containing_no_self_containing_u_is_bisimilar(self):
        for u_self, u_has_s, u_real in itertools.product([False, True], repeat=3):
            if u_self or u_has_s:
                self.assertFalse(bisimilar(False, u_self, u_has_s, u_real),
                                 (u_self, u_has_s, u_real))

    def test_s_alone_can_still_match_a_u_that_holds_no_copy(self):
        self.assertTrue(bisimilar(False, False, False, True))


class PresentationsOfUTests(unittest.TestCase):
    def test_one_two_three_node_presentations_are_one_object_and_not_s(self):
        nodes, edges = ["S"] + R, [("S", r) for r in R]
        heads = {}
        for k in (1, 2, 3):
            ns, es = ring(k, f"k{k}_")
            nodes, edges = nodes + ns, edges + es
            heads[k] = ns[0]
        part = bisimulation_classes(nodes, edges)
        self.assertEqual(len({part[heads[k]] for k in (1, 2, 3)}), 1)
        self.assertNotEqual(part[heads[1]], part["S"])

    def test_every_node_of_a_ring_is_in_the_same_block(self):
        nodes, edges = ring(3, "u")
        nodes, edges = nodes + ["S"] + R, edges + [("S", r) for r in R]
        part = bisimulation_classes(nodes, edges)
        self.assertEqual(len({part[f"u{i}"] for i in range(3)}), 1)

    def test_negative_control_broken_ring_is_not_one_object(self):
        # Remove S from one node of the 2-ring: that node is not bisimilar to
        # the other, so the collapse is not automatic.
        nodes, edges = ring(2, "u")
        nodes, edges = nodes + ["S"] + R, edges + [("S", r) for r in R]
        edges = [e for e in edges if e != ("u1", "S")]
        part = bisimulation_classes(nodes, edges)
        self.assertNotEqual(part["u0"], part["u1"])


if __name__ == "__main__":
    unittest.main()
