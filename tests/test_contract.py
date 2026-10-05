"""Independent finite counterexamples for the proposed Hyperreality frame."""

import unittest

import hyperreality
from hyperreality import (DECLARED_KINDS, Classification, Containment, Kind,
                          Presentation, Registry, Whole, classes_of,
                          containers_of, instances_of_kind, members_of,
                          resolve_kind, well_founded)


def four_kinds():
    return tuple(k for k in DECLARED_KINDS
                 if k.name in {"base-reality", "areality", "surreality", "preality"})


class KindDisciplineTests(unittest.TestCase):
    def test_declared_kinds_are_pairwise_distinct(self):
        names = [k.name for k in DECLARED_KINDS]
        self.assertEqual(len(names), len(set(names)))
        for name in ("base-reality", "areality", "surreality", "preality"):
            self.assertIn(name, names)

    def test_kinds_carry_no_rank_or_order(self):
        a, b = four_kinds()[:2]
        with self.assertRaises(TypeError):
            _ = a < b
        for forbidden in ("rank", "order", "more_real", "degree"):
            self.assertFalse(hasattr(hyperreality, forbidden), forbidden)

    def test_kind_list_is_open(self):
        extra = Kind("hypothetical-fifth", "test-only declaration", "TEST")
        reg = Registry(four_kinds() + (extra,),
                       (Presentation("x", "hypothetical-fifth"),))
        self.assertEqual(instances_of_kind(reg, "hypothetical-fifth"), frozenset({"x"}))

    def test_reality_is_not_silently_aliased_to_base_reality(self):
        reg = Registry(four_kinds(), (Presentation("b1", "base-reality"),))
        with self.assertRaises(KeyError):
            resolve_kind(reg, "reality")
        with self.assertRaises(ValueError):
            Registry(four_kinds(), (Presentation("r1", "reality"),))

    def test_every_declared_kind_names_its_source(self):
        for kind in DECLARED_KINDS:
            self.assertTrue(kind.gloss and kind.source, kind.name)


class TwoRelationTests(unittest.TestCase):
    """Classification (is-a) and containment (is-in) never imply each other."""

    def setUp(self):
        self.kinds = four_kinds()
        self.people = (Presentation("b1", "base-reality"), Presentation("d1", "surreality"))

    def test_classification_does_not_contain(self):
        reg = Registry(self.kinds, self.people, (Whole("s1", "sempiternality"),),
                       classifications=(Classification("b1", "sempiternality"),))
        self.assertEqual(classes_of(reg, "b1"), frozenset({"sempiternality"}))
        self.assertEqual(containers_of(reg, "b1"), frozenset())
        self.assertEqual(members_of(reg, "s1"), frozenset())

    def test_containment_does_not_classify(self):
        reg = Registry(self.kinds, self.people, (Whole("s1", "sempiternality"),),
                       containments=(Containment("s1", "b1"),))
        self.assertEqual(containers_of(reg, "b1"), frozenset({"s1"}))
        self.assertEqual(classes_of(reg, "b1"), frozenset())

    def test_containment_endpoints_must_exist(self):
        with self.assertRaises(ValueError):
            Registry(self.kinds, self.people, (), containments=(Containment("s9", "b1"),))
        with self.assertRaises(ValueError):
            Registry(self.kinds, self.people, (), containments=(Containment("b1", "b1"),))


class SempiternityDirectionTests(unittest.TestCase):
    """09-26: a sempiternity contains realities. 09-29: a base-reality contains
    a sempiternity. The frame decides neither; it shows what each costs."""

    def setUp(self):
        self.kinds = four_kinds()
        self.base = (Presentation("b1", "base-reality"),)

    def test_both_readings_hold_of_two_distinct_wholes(self):
        reg = Registry(self.kinds, self.base,
                       (Whole("s-outer", "sempiternality"), Whole("s-inner", "sempiternality")),
                       containments=(Containment("s-outer", "b1"), Containment("b1", "s-inner")))
        self.assertTrue(well_founded(reg))
        self.assertEqual(containers_of(reg, "s-inner"), frozenset({"b1", "s-outer"}))

    def test_both_readings_of_one_whole_is_not_well_founded(self):
        reg = Registry(self.kinds, self.base, (Whole("s1", "sempiternality"),),
                       containments=(Containment("s1", "b1"), Containment("b1", "s1")))
        self.assertFalse(well_founded(reg))
        self.assertIn("s1", containers_of(reg, "s1"))


class BaseRealityMultiplicityTests(unittest.TestCase):
    def test_grid_of_base_realities_is_representable(self):
        reg = Registry(four_kinds(), tuple(Presentation(f"b{i}", "base-reality")
                                           for i in range(3)))
        self.assertEqual(len(instances_of_kind(reg, "base-reality")), 3)


class RegistryBoundsTests(unittest.TestCase):
    def test_duplicate_identities_are_rejected(self):
        with self.assertRaises(ValueError):
            Registry(four_kinds(), (Presentation("a", "areality"),
                                    Presentation("a", "preality")))
        with self.assertRaises(ValueError):
            Registry(four_kinds(), (Presentation("a", "areality"),),
                     (Whole("a", "sempiternality"),))

    def test_duplicate_kind_names_are_rejected(self):
        k = four_kinds()[0]
        with self.assertRaises(ValueError):
            Registry((k, k), ())


if __name__ == "__main__":
    unittest.main()
