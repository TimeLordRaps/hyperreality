# Hyperreality

**What a reality is, and which kinds of reality there are.** Tyler Roost /
The TimeLord orders the kinds by control: with each layer one must first gain
control of the layers below it (his statement of 2026-10-05, in
[PROVENANCE.md](PROVENANCE.md)). Lowest first:

1. **base-reality**, "N-d universal base reality".
2. **surreality**, dream control: lucid and controllable dreamscapes.
3. **areality**, artificial realities unobservably indifferent from a base
   reality, which a person enters by mind linking, either consciously through
   apparatus (like playing a character inside it while the body spends no
   wall-clock time) or asynchronously by upload.
4. **preality**, the possibility reality. It arises only when we try to link
   into our own reality: an automatic research loop that manipulates base
   reality from the linked simulation, where each manipulation teaches more of
   the natural laws unobservable from base reality alone.
5. **hypergeometric reality**, the proposed kind.
6. **oreality**, the transfinite-dimensional reality that exists naturally as a
   consequence of hypergeometric reality existing, around it or within it
   (which of the two is open).
7. **sempiternity**, the object that holds the property sempiternality;
   unbounded in time.
8. **universempiternity**, the superstructure: it contains all the kinds below
   it, sempiternity, and itself.

The list is open. Oreality's older gloss, "springs out from areality", is the
2026-09-23 statement and is superseded in its placement by the order above.
The taxonomy is [HYPER]; the finite reading is a [FRAME]. The kinds were first
declared in Hyperethics, and whether that text moves here is open (Q4 in
[FIELD_SPEC.md](FIELD_SPEC.md)).

The [finite Python frame](hyperreality.py) keeps these disciplines:

- **The order is a control prerequisite, not a degree of reality.** It is
  `CONTROL_ORDER`, with `control_prerequisites` and `controlled_before`.
  Comparing two `Kind` objects still raises, and there is no rank or degree.
- **No silent aliasing.** `reality` is not quietly `base-reality`.
- **Is-a and is-in stay apart.** Classifying a reality never places it in a
  container, and containing a reality never classifies it. The order is
  neither.

[Tests](tests/test_contract.py) include a finite witness on the open
question of direction: whether a sempiternity contains base-reality, or a
base-reality contains a sempiternity. Both readings can hold of two
distinct wholes. One whole in both roles is not well-founded.

Further tests port the owner's mapping of kinds to reality classes, a
bisimilarity check between a sempiternity and its container, and a finite
toy of anchoring preality (see [FIELD_SPEC.md](FIELD_SPEC.md)), and the
control order ([tests](tests/test_control_order.py)). Which way his
"inherits upward, supports from underneath" arrows point against this order is
still open (HR-013).

Reality as a situated slice belongs to
[Hyperstratum](https://github.com/TimeLordRaps/hyperstratum). Observability
belongs to [Hyperspace](https://github.com/TimeLordRaps/hyperspace), and
order to [Hypertime](https://github.com/TimeLordRaps/hypertime). This
repository cites them and does not restate them. [FIELD.json](FIELD.json)
is a local integration descriptor, not a Verifier Standard (VSTD)
certificate.

Run the standard-library suite with `python -u validate.py`. The runner
streams named tests under a 20-second overall deadline. It has no per-test
process isolation. Open questions are in [FIELD_SPEC.md](FIELD_SPEC.md),
sources in [PROVENANCE.md](PROVENANCE.md), obligations in
[TECHNICAL_DEBT.md](TECHNICAL_DEBT.md), and the next step in
[AGENT_HANDOFF.md](AGENT_HANDOFF.md).
