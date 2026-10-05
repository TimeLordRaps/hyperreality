# Hyperreality: what a reality is, and which kinds there are

**Status, 2026-09-29.** [FRAME] Hyperreality studies what a reality is and
which kinds of reality there are. Tyler Roost has declared a taxonomy of
reality kinds (base-reality, areality, surreality, preality, later
oreality, and a proposed hypergeometric reality) and a sempiternity (the object) that
is their container, with the property it holds, sempiternality, as their class. This repository is
proposed as the family's home for those declarations, and it states the
discipline they already carry. Whether the declaring text moves here is Q4.
It does not settle the questions the declarations leave open. Tags: [HYPER]
Tyler's proposal, [FRAME] the finite executable reading, [OPEN] unresolved,
[FORM] a structural fact the tests check.

## What this field owns, and what it cites

Hyperreality owns **reality presentations** and the
**classification/containment discipline** for realities and sempiternity.
The **kind taxonomy** is declared today in hyperethics L3. This field lists
the kinds by name, each with its source, and cites L3 for the declaration.
Whether the taxonomy itself moves here is Q4.

It cites and does not restate:

| Subject | Owner |
|---|---|
| The declaration of the kinds, until Q4 is answered | [Hyperethics](https://github.com/TimeLordRaps/hyperethics) L3 |
| Reality as a situated slice; the shared vocabulary | [Hyperstratum](https://github.com/TimeLordRaps/hyperstratum/blob/ecf972f289d6e269e302638856227b3e3f85ac6d/specs/canonical-definitions.md) |
| Placement and observability among presentations | [Hyperspace](https://github.com/TimeLordRaps/hyperspace) |
| Order and branching among presentations | [Hypertime](https://github.com/TimeLordRaps/hypertime) |
| Objects, and perspective | Hyperobjectivity; Hypersubjectivity |
| General relation types (is-a, is-in, composition as structure) | Hyperstructure |
| Mechanisms and dynamics that move between realities | Hypermechanics; Hyperdynamics |
| A thought's reality being areality; Realm as creation's ground | [Hyperethics](https://github.com/TimeLordRaps/hyperethics) L3 and L0 |
| Oreality × hyperprobability (a transport between two fields) | [Metamathethicology](https://github.com/TimeLordRaps/metamathethicology/tree/846ce08de66f452d3942eea3d5aedbd8a03bbf47) |

## Kinds

[HYPER] The declared kinds and their sources are in
[PROVENANCE.md](PROVENANCE.md) and `DECLARED_KINDS` in
[hyperreality.py](hyperreality.py).

[FORM] The following hold of the kinds, and the tests check each one:

- Kinds are pairwise distinct.
- Kinds are **unordered**. Comparing two kinds raises an error, and the
  module exports no rank, order, or degree. "Separate" is the whole of the
  relation between kinds.
- The list is **open**. A registry may declare a further kind, with its own
  source, and it is accepted on equal terms.
- A kind is resolved by **exact name only**. There is no alias table. In
  particular, `reality` does not resolve to `base-reality`.

[OPEN] Two local drafts elsewhere in the family disagree on that last point.
One maps `reality` to `base-reality` "for this finite integration role only".
The other calls the mapping open, "not an implicit alias". This field takes
the stricter reading until Tyler rules. The alias can be added as a
declared, sourced entry. It cannot be reintroduced silently.

## Two relations, never inferred from each other

[FRAME] `Classification(member, class)` is **is-a**. `Containment(container,
member)` is **is-in**. A classification never places anything in a
container, and a containment never classifies anything. Tyler's 2026-09-26
statement makes one word, then spelled sempiternality, both the abstract class and the container
class of the reality kinds. Since 2026-10-05 the class role is the property sempiternality
and the container role is the object, a sempiternity. That is exactly why the two relations are held
apart: each role is stated separately and checked separately.

A `Whole` is an instance of a class that is not itself a reality kind, such
as one sempiternity.

## The direction question, as a finite witness

[HYPER] On 2026-09-26, a sempiternity contains realities. On 2026-09-29, a
base-reality expands to obtain a sempiternity inside itself.

[FORM] The tests show what each reading costs, without choosing:

- **Two distinct sempiternity wholes.** One contains base-reality `b1`,
  and `b1` contains the other. Both statements hold together, and
  containment stays well-founded.
- **One and the same whole.** If it both contains and is contained by `b1`,
  containment is **not** well-founded.

Well-foundedness is **reported, not enforced**. A registry in which
containment loops can still be built and inspected.

[OPEN] Q2 below asks which reading Tyler intends, or whether both hold at
different levels.

## Multiplicity

[FORM] Any number of presentations of one kind are allowed, so several
base-realities can sit in a grid. The kinds do not conflict with a grid:
base-reality is a kind, and nothing limits how many realities have it.
[OPEN] Q1 asks what Tyler intends. His 09-21 words, quoted in hyperethics
L3, say "N-d universal base reality" with no article; L3's own glosses add
"the". His 09-28 words, in Hyperspace, say "a bunch of base realities in a
grid". Nothing here assumes uniqueness.

## Open questions only Tyler can answer

1. Is base-reality one N-d universal base, or many in a grid? And is our 4D
   reality itself a base-reality, or only, in the 09-23 words, "the 4D
   projection of possibility reality"?
2. Does a sempiternity contain base-reality (09-26), does a base-reality
   contain a sempiternity (09-29), or do both hold at different levels?
3. Which field owns sempiternity and universempiternity: this one or
   Hyperstructure?
4. Should the kind declarations stay in hyperethics L3, with this field
   citing them, or move here? Hyperethics imports no other field: its
   README lists no dependencies, and L3's header sends any borrowing of
   another field's subject to metamathethicology. So a move also takes
   `ax-thought-is-areal` out of hyperethics, because that axiom names the
   kind `areality`. It would become a transport between the two fields,
   placed in metamathethicology.
5. Does "realities are that which are observable" replace, or sharpen,
   Hyperstratum's situated slice?
6. Is a superposition reading of surreality the same kind as the dream
   reality, or a further kind?
7. Hyperethics uses `Realm` for creation's ground (L0), and its L3 says a
   Reality is never a Realm. The oreality combination field uses `Realm`
   for its own record of one declared realm, a type neither parent
   contains. No code collides, since oreality imports neither parent. Is the
   shared word acceptable, or should one be renamed so that L0's meaning is
   not read into oreality's realms?
8. Should the declared claim that our universe is a simulation live here, as
   a declared and unadjudicated claim?
9. Another draft in the family uses "hyperreality" as a second name for
   universempiternity. Is universempiternity this field's subject, one
   subject within it, or a different thing that should keep its own name?
10. What is hypergeometric reality? It is recorded as proposed, and no
    public definition exists. Its relation to the Hypergeometry field is
    also open.

These are tracked as HR-001 to HR-010 in [TECHNICAL_DEBT.md](TECHNICAL_DEBT.md).
