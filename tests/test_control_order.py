"""The owner's control order of the kinds (USER-STATED 2026-10-05)."""
import unittest

import hyperreality
from hyperreality import (CONTROL_ORDER, DECLARED_KINDS, Containment, Registry,
                          control_position, control_prerequisites, controlled_before,
                          members_of, order_is_declared)

EXPECTED = ("base-reality", "surreality", "areality", "preality",
            "hypergeometric-reality", "oreality", "sempiternity", "universempiternity")


class ControlOrderTests(unittest.TestCase):
    def test_order_is_exactly_the_owners_list(self):
        self.assertEqual(CONTROL_ORDER, EXPECTED)

    def test_every_declared_kind_is_placed_once_and_nothing_else(self):
        self.assertTrue(order_is_declared())
        self.assertFalse(order_is_declared(DECLARED_KINDS[:-1]))  # negative control

    def test_strict_total_order(self):
        names = CONTROL_ORDER
        for a in names:
            self.assertFalse(controlled_before(a, a))
            for b in names:
                if a != b:
                    self.assertNotEqual(controlled_before(a, b), controlled_before(b, a))
                for c in names:
                    if controlled_before(a, b) and controlled_before(b, c):
                        self.assertTrue(controlled_before(a, c))

    def test_prerequisites_are_all_lower_layers_bottom_first(self):
        self.assertEqual(control_prerequisites("base-reality"), ())
        self.assertEqual(control_prerequisites("preality"),
                         ("base-reality", "surreality", "areality"))
        self.assertEqual(control_prerequisites("universempiternity"), EXPECTED[:-1])

    def test_oreality_sits_between_hypergeometric_reality_and_sempiternity(self):
        self.assertEqual(control_position("oreality") - control_position("hypergeometric-reality"), 1)
        self.assertEqual(control_position("sempiternity") - control_position("oreality"), 1)

    def test_unplaced_kind_is_refused_not_guessed(self):
        with self.assertRaises(KeyError):
            control_position("reality")

    def test_order_is_not_containment_and_not_a_degree(self):
        reg = Registry(DECLARED_KINDS, ())
        self.assertEqual(reg.containments, ())
        self.assertEqual(members_of(reg, "base-reality"), frozenset())
        for forbidden in ("rank", "more_real", "degree"):
            self.assertFalse(hasattr(hyperreality, forbidden), forbidden)

    def test_kind_objects_still_do_not_compare(self):
        with self.assertRaises(TypeError):
            _ = DECLARED_KINDS[0] < DECLARED_KINDS[1]


if __name__ == "__main__":
    unittest.main()
