"""Counterparts as a third relation, areality simulation, and the preality law (2026-10-05/06)."""
import unittest

import hyperreality
from hyperreality import (CONTROL_ORDER, DECLARED_KINDS, KINDS_WITH_ATEMPORAL_COUNTERPART,
                          OBTAINABLE_FROM_PREALITY, SIMULABLE_IN_AREALITY, Classification,
                          Containment, Counterpart, Presentation, Registry, Whole,
                          areality_can_simulate, atemporal_of, classes_of, containers_of,
                          control_position, counterpart_law_violations, members_of,
                          temporal_of)

PRES = (Presentation("b1", "base-reality"), Presentation("b1-null", "base-reality"),
        Presentation("a1", "areality"), Presentation("a1-null", "areality"),
        Presentation("p1", "preality"), Presentation("p1-null", "preality"),
        Presentation("s1", "surreality"), Presentation("s1-null", "surreality"))
WHOLES = (Whole("S", "sempiternality"),)
PAIRS = (Counterpart("b1", "b1-null"), Counterpart("a1", "a1-null"),
         Counterpart("p1", "p1-null"), Counterpart("s1", "s1-null"))
INSIDE = tuple(Containment("S", t) for t in ("b1-null", "a1-null", "p1-null", "s1-null"))


def reg(**kw):
    base = dict(kinds=DECLARED_KINDS, presentations=PRES, wholes=WHOLES,
                counterparts=PAIRS, containments=INSIDE)
    base.update(kw)
    return Registry(**base)


class CounterpartRelationTests(unittest.TestCase):
    def test_counterpart_is_neither_is_a_nor_is_in(self):
        with_pairs, without = reg(), reg(counterparts=())
        for ident in ("b1", "b1-null", "a1", "p1"):
            self.assertEqual(classes_of(with_pairs, ident), classes_of(without, ident))
            self.assertEqual(containers_of(with_pairs, ident), containers_of(without, ident))
            self.assertEqual(members_of(with_pairs, ident), members_of(without, ident))

    def test_lookup_both_ways_and_no_inference(self):
        r = reg()
        self.assertEqual(atemporal_of(r, "b1"), "b1-null")
        self.assertEqual(temporal_of(r, "b1-null"), "b1")
        self.assertIsNone(atemporal_of(r, "b1-null"))
        r2 = reg(counterparts=(), containments=())
        self.assertIsNone(atemporal_of(r2, "b1"))  # sharing a kind and a container is not enough

    def test_counterparts_present_the_same_kind(self):
        with self.assertRaises(ValueError):
            reg(counterparts=(Counterpart("b1", "a1-null"),))

    def test_endpoints_must_be_presented_realities(self):
        with self.assertRaises(ValueError):
            reg(counterparts=(Counterpart("b1", "S"),))      # a Whole is not a presented reality
        with self.assertRaises(ValueError):
            reg(counterparts=(Counterpart("b1", "nowhere"),))

    def test_functional_both_ways_and_no_self(self):
        with self.assertRaises(ValueError):
            Counterpart("b1", "b1")
        with self.assertRaises(ValueError):
            reg(counterparts=(Counterpart("b1", "b1-null"), Counterpart("b1", "b1-null2")),
                presentations=PRES + (Presentation("b1-null2", "base-reality"),))
        with self.assertRaises(ValueError):
            reg(counterparts=(Counterpart("b1", "b1-null"), Counterpart("a1", "b1-null")))

    def test_classification_is_still_not_inferred_from_counterpart(self):
        r = reg(classifications=(Classification("b1", "sempiternality"),))
        self.assertEqual(classes_of(r, "b1-null"), frozenset())


class PrealityLawTests(unittest.TestCase):
    def test_law_holds_when_every_listed_reality_has_a_twin_inside_a_sempiternity(self):
        self.assertEqual(counterpart_law_violations(reg()), ())

    def test_missing_counterpart_is_reported_negative_control(self):
        r = reg(counterparts=PAIRS[1:], containments=INSIDE[1:])
        # b1 lost its twin, and the orphaned b1-null is now a base-reality with none either
        self.assertEqual(set(counterpart_law_violations(r)),
                         {("b1", "no atemporal counterpart"), ("b1-null", "no atemporal counterpart")})
        pres = tuple(p for p in PRES if p.reality_id != "b1-null")
        r2 = reg(presentations=pres, counterparts=PAIRS[1:], containments=INSIDE[1:])
        self.assertEqual(counterpart_law_violations(r2), (("b1", "no atemporal counterpart"),))

    def test_twin_outside_every_sempiternity_is_reported_negative_control(self):
        r = reg(containments=INSIDE[1:])
        self.assertEqual(counterpart_law_violations(r),
                         (("b1", "atemporal counterpart is not within a sempiternity"),))

    def test_twin_inside_a_non_sempiternity_whole_does_not_count(self):
        r = reg(wholes=WHOLES + (Whole("X", "other"),), containments=(Containment("X", "b1-null"),) + INSIDE[1:])
        self.assertEqual(len(counterpart_law_violations(r)), 1)

    def test_kinds_without_a_stated_counterpart_are_not_required_to_have_one(self):
        r = reg(presentations=PRES + (Presentation("o1", "oreality"), Presentation("h1", "hypergeometric-reality")))
        self.assertEqual(counterpart_law_violations(r), ())

    def test_listed_kinds_are_the_four_the_owner_named(self):
        self.assertEqual(set(KINDS_WITH_ATEMPORAL_COUNTERPART),
                         {"base-reality", "surreality", "areality", "preality"})
        self.assertTrue(all(k in CONTROL_ORDER for k in KINDS_WITH_ATEMPORAL_COUNTERPART))


class SimulationTests(unittest.TestCase):
    def test_areality_simulates_every_kind_below_sempiternity_including_itself(self):
        for kind in CONTROL_ORDER[:control_position("sempiternity")]:
            self.assertTrue(areality_can_simulate(kind), kind)
        self.assertTrue(areality_can_simulate("areality"))

    def test_sempiternity_and_above_are_not_simulated_negative_control(self):
        self.assertFalse(areality_can_simulate("sempiternity"))
        self.assertFalse(areality_can_simulate("universempiternity"))

    def test_unplaced_kind_is_refused_not_guessed(self):
        with self.assertRaises(KeyError):
            areality_can_simulate("reality")

    def test_simulation_is_not_control_order(self):
        # Preality sits above areality in the control order (control areality first), yet an
        # areality device simulates it: representation runs the other way from control.
        self.assertTrue(control_position("areality") < control_position("preality"))
        self.assertTrue(areality_can_simulate("preality"))
        self.assertTrue(areality_can_simulate("oreality"))
        self.assertEqual(SIMULABLE_IN_AREALITY, CONTROL_ORDER[:6])

    def test_obtainable_from_preality(self):
        self.assertEqual(OBTAINABLE_FROM_PREALITY, ("base-reality", "surreality"))
        for kind in OBTAINABLE_FROM_PREALITY:
            self.assertTrue(control_position(kind) < control_position("preality"))
            self.assertTrue(areality_can_simulate(kind))

    def test_simulating_is_neither_containing_nor_classifying(self):
        for name in ("simulates", "simulated_by"):
            self.assertFalse(hasattr(hyperreality, name))
        r = Registry(DECLARED_KINDS, PRES, WHOLES)
        self.assertEqual(containers_of(r, "p1"), frozenset())
        self.assertEqual(classes_of(r, "p1"), frozenset())


if __name__ == "__main__":
    unittest.main()
