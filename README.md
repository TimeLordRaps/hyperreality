# Hyperreality

**What a reality is, and which kinds of reality there are.** Tyler Roost /
The TimeLord separates reality into kinds that have no ranking between them:

- base-reality, "N-d universal base reality";
- areality, the abstract artificial reality;
- surreality, the dream reality;
- preality, the possibility reality;
- oreality, which springs out from areality;
- a proposed hypergeometric reality.

The list is open. He also names a sempiternality that is both their abstract
class and their container. This repository is proposed as the family's home
for those declarations. The kinds are declared today in Hyperethics, and
whether that text moves here is open (Q4 in [FIELD_SPEC.md](FIELD_SPEC.md)).
The taxonomy is [HYPER]; the finite reading is a [FRAME].

The [finite Python frame](hyperreality.py) keeps three disciplines:

- **No ranking.** Kinds cannot be compared or ordered.
- **No silent aliasing.** `reality` is not quietly `base-reality`.
- **Is-a and is-in stay apart.** Classifying a reality never places it in a
  container, and containing a reality never classifies it.

[Tests](tests/test_contract.py) include a finite witness on the open
question of direction: whether sempiternality contains base-reality, or a
base-reality contains a sempiternality. Both readings can hold of two
distinct wholes. One whole in both roles is not well-founded.

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
