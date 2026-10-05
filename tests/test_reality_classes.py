"""The owner's reality-class mapping expressed as a Registry (USER-STATED
2026-10-04; see PROVENANCE.md). Ported from the Hyperstratum incubator check
hm-top/reality_classes.py. The mapping itself is [HYPOTHETICAL]; the facts
checked here are [FORM] facts about this finite frame."""

import unittest

import hyperreality
from bisim_helper import bisimulation_classes, containment_graph
from hyperreality import (Classification, Containment, Kind, Presentation,
                          Registry, Whole, classes_of, members_of, well_founded)

BASE = Kind("base-reality", "normal, rational and irrational representations",
            "USER-STATED 2026-10-04")
SUR = Kind("surreality", "surreal representations", "USER-STATED 2026-10-04")
ARE = Kind("areality", "imaginary representations", "USER-STATED 2026-10-04")
KINDS = (BASE, SUR, ARE)

REALITIES = (
    Presentation("r-normal", "base-reality"),
    Presentation("r-rational", "base-reality"),
    Presentation("r-irrational", "base-reality"),
    Presentation("r-surreal", "surreality"),
    Presentation("r-imaginary", "areality"),
)
S = Whole("S", "sempiternality")  # the object; its class is the property
S_CONTAINS = tuple(Containment("S", p.reality_id) for p in REALITIES)


def loop_registry(extra=()):
    """Two-node loop: U1 and U2 each contain S and each other."""
    wholes = (S, Whole("U1", "universempiternality"),
              Whole("U2", "universempiternality"))
    loop = (Containment("U1", "S"), Containment("U1", "U2"),
            Containment("U2", "S"), Containment("U2", "U1"))
    return Registry(KINDS, REALITIES, wholes, containments=S_CONTAINS + loop + extra)


class MappingIsExpressibleTests(unittest.TestCase):
    def test_sempiternity_is_a_whole_of_class_sempiternality(self):
        self.assertEqual((S.whole_id, S.class_name), ("S", "sempiternality"))

    def test_sempiternity_contains_the_realities_and_classifies_nothing(self):
        reg = Registry(KINDS, REALITIES, (S,), containments=S_CONTAINS)
        self.assertTrue(well_founded(reg))
        self.assertEqual(members_of(reg, "S"),
                         frozenset(p.reality_id for p in REALITIES))
        self.assertEqual(classes_of(reg, "S"), frozenset())

    def test_containing_does_not_classify_the_realities(self):
        reg = Registry(KINDS, REALITIES, (S,), containments=S_CONTAINS)
        for p in REALITIES:
            self.assertEqual(classes_of(reg, p.reality_id), frozenset())

    def test_classification_is_never_inferred_from_containment_negative_control(self):
        # Only an explicit Classification yields a class.
        reg = Registry(KINDS, REALITIES, (S,), containments=S_CONTAINS,
                       classifications=(Classification("r-normal", "sempiternality"),))
        self.assertEqual(classes_of(reg, "r-normal"), frozenset({"sempiternality"}))
        self.assertEqual(classes_of(reg, "r-rational"), frozenset())


class KindObjectsDoNotCompareTests(unittest.TestCase):
    def test_comparison_of_every_pair_raises(self):
        for a, b in ((BASE, SUR), (SUR, ARE), (BASE, ARE)):
            with self.assertRaises(TypeError):
                _ = a < b
            with self.assertRaises(TypeError):
                _ = a >= b

    def test_module_exports_no_rank_or_degree(self):
        for forbidden in ("rank", "more_real", "degree"):
            self.assertFalse(hasattr(hyperreality, forbidden), forbidden)

    def test_number_classes_nesting_is_not_inclusion_between_kinds(self):
        # The number classes the kinds are mapped to nest (ordinals within
        # surreals within surcomplex numbers), but the registry has no
        # containment between kinds: kinds are not identities, so a
        # containment naming one is refused.
        for a, b in (("base-reality", "surreality"), ("surreality", "areality")):
            with self.assertRaises(ValueError):
                Registry(KINDS, REALITIES, (S,), containments=(Containment(a, b),))


class SelfContainingTopTests(unittest.TestCase):
    def test_one_node_loop_is_refused_as_direct_self_containment(self):
        with self.assertRaises(ValueError):
            Containment("U", "U")

    def test_two_node_loop_is_accepted_and_not_well_founded(self):
        reg = loop_registry()
        self.assertFalse(well_founded(reg))

    def test_two_node_loop_is_bisimilar_to_itself_collapsed(self):
        nodes, edges = containment_graph(loop_registry())
        part = bisimulation_classes(nodes, edges)
        self.assertEqual(part["U1"], part["U2"])
        self.assertNotEqual(part["U1"], part["S"])

    def test_two_node_loop_matches_the_one_node_loop_as_a_graph(self):
        # The one-node loop cannot be a Containment, so it is written as a
        # bare graph, which the helper accepts. The two presentations agree
        # up to bisimilarity.
        leaves = [p.reality_id for p in REALITIES]
        nodes = ["S", "U"] + leaves
        edges = ([("S", r) for r in leaves] + [("U", "S"), ("U", "U")]
                 + [("U", r) for r in leaves])
        one = bisimulation_classes(nodes, edges)
        n2, e2 = containment_graph(loop_registry())
        two = bisimulation_classes(n2, e2)
        # Same number of blocks once U1/U2 are identified: leaf block, S, U.
        self.assertEqual(len(set(one.values())), 3)
        self.assertEqual(len(set(two.values())), 3)

    def test_negative_control_extra_member_breaks_bisimilarity(self):
        reg = loop_registry(extra=(Containment("U2", "r-normal"),))
        nodes, edges = containment_graph(reg)
        part = bisimulation_classes(nodes, edges)
        self.assertNotEqual(part["U1"], part["U2"])

    def test_negative_control_one_sided_loop_is_not_bisimilar(self):
        wholes = (S, Whole("U1", "universempiternality"),
                  Whole("U2", "universempiternality"))
        reg = Registry(KINDS, REALITIES, wholes, containments=S_CONTAINS + (
            Containment("U1", "S"), Containment("U1", "U2"), Containment("U2", "U1")))
        nodes, edges = containment_graph(reg)
        part = bisimulation_classes(nodes, edges)
        self.assertNotEqual(part["U1"], part["U2"])

    def test_helper_rejects_unknown_nodes(self):
        with self.assertRaises(ValueError):
            bisimulation_classes(["a"], [("a", "b")])


if __name__ == "__main__":
    unittest.main()
