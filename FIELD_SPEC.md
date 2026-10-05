# Hyperreality: what a reality is, and which kinds there are

**Status, 2026-09-29; sections on reality classes, naming, time sense, counterparts, order and anchoring added 2026-10-05.** [FRAME] Hyperreality studies what a reality is and
which kinds of reality there are. Tyler Roost has declared a taxonomy of
reality kinds, ordered by control from the bottom: base-reality, surreality,
areality, preality, hypergeometric reality, oreality, sempiternity, universempiternity (2026-10-05),
and a sempiternity (the object) that is their container, with the property it holds, sempiternality, as their class. This repository is
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
- Kinds are ordered by **control** (2026-10-05, supersedes the 2026-09-21
  "unordered" rule): `CONTROL_ORDER` lists them lowest first, and each layer
  is reached by first gaining control of those below. The order is an explicit
  declaration. Comparing two `Kind` objects still raises, and the module
  exports no rank or degree: it is a prerequisite relation, not "more real".
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

## Reality classes

[HYPOTHETICAL] On 2026-10-04 Tyler mapped kinds to classes of number-like representations: base-reality to normal, with rational and irrational both in base-reality; surreality to surreal; areality to imaginary; and the sempiternity encompassing them (quotation in [PROVENANCE.md](PROVENANCE.md)). The mapping is his. What this field can check is its finite expression, in `tests/test_reality_classes.py`:

- [FORM] It is expressible. A sempiternity is a `Whole` whose `class_name` is `sempiternality`. It contains the realities and classifies nothing, and containment stays well-founded.
- [FORM] Kind objects stay non-comparable (the control order is separate, declared in `CONTROL_ORDER`), although the number classes they are mapped to nest (ordinals within surreals within surcomplex numbers). Comparing two kinds still raises, and a containment between kinds is refused, since kinds are not identities.
- [FORM] A universempiternity written as one node containing itself is **refused**: `Containment` forbids direct self-containment. A two-node loop, each node containing the sempiternity and the other, is accepted and reported not well-founded. It is bisimilar to the one-node loop by partition refinement. A one-sided loop is not bisimilar, and neither is a loop in which one node has an extra member (negative controls).
- [OPEN] Whether the mapping is classification only, with no inclusion between kinds, or whether the "no order, no nesting" rule needs revisiting (HR-017).

## Object and property

[HYPER] A **sempiternity** is the object, the whole that contains the realities. **Sempiternality** is the property it holds, the class it belongs to. Tyler decided this on 2026-10-05, and the `Whole` class name already has that shape. The same split by analogy for the self-containing top (a universempiternity holding universempiternality) is not stated by him and stays [HYPOTHETICAL]. Why the two relations stay apart is in the section above on classification and containment.

## Whether S contains itself

[FORM] In a finite containment model, S and U are bisimilar exactly when U contains the realities directly (containment closed transitively) and S holds a copy of the whole exactly when U does. `tests/test_sempiternity_bisim.py` enumerates all 16 combinations of four clauses (S contains S, U contains U, U contains S, U contains the realities) against that criterion, with a mutation control that rejects a wrong predicate. Consequences, all of the finite model:

- The case where only U contains S and itself, with S containing neither, is **not** bisimilar. Give S a self-containing copy and it is.
- S need not contain itself. If it does not, S is bisimilar to no U that contains itself or contains S, so they are different objects.
- U is still determined: its one-, two- and three-node presentations are one object up to `==`, and that object is not S.

[OPEN] Whether the family intends the transitive closure in the first clause. [HYPOTHETICAL] as a reading of universempiternity.

## Time sense

[HYPER] Tyler stated on 2026-10-05 that sempiternity is unbounded in time. Wording elsewhere in the family that calls sempiternity atemporal (this field's 2026-09-26 record, and Hypertime's field specification) can therefore describe, at most, the atemporal counterparts below. The earlier records stay visible and are marked superseded in scope. [OPEN] For universempiternity he did not say.

## Counterparts

[HYPER] As stated on 2026-10-05, three kinds each have a temporal and an atemporal counterpart:

| Kind | Temporal | Atemporal |
|---|---|---|
| surreality | first-person dreaming | dream architecting |
| preality | not stated | the laws of base realities, including time and retrocausality, in representable form |
| base-reality | an instantiation, at one time, of the observable physical laws | not stated |

[OPEN] Two cells are not stated, and areality is not mentioned. [FORM] The registry has two relations, is-a and is-in, and no way to say "counterpart of". The table is not expressible here and is not encoded. Reading it as is-a or is-in would break the rule that the two relations are never inferred from each other (HR-014, HR-015).

## Order among the realities

[HYPER] On 2026-10-04 Tyler said an order to the realities has since been established, and that hyperorder may be needed to describe it (quotation in [PROVENANCE.md](PROVENANCE.md)). His 2026-10-05 answer: "I think its inherits upward and supports from underneath btw".

[OPEN] Read with his 2026-10-04 hierarchy (prealities run inside the sempiternity; surreality inherits from them through an imagination-reachable filter; base-reality is beneath and holds access to the higher ones), the answer gives two relations on one ladder: inherits-from, pointing up from a lower kind to a higher one, and supports, given by the lower kind to the higher. Whether that is the intended reading of the arrows is not settled, and his two phrases do not say which kind is the source of each (HR-013).

[FRAME] Superseded 2026-10-05: Tyler gave the order in encodable form, a control order on kinds (base-reality, surreality, areality, preality, hypergeometric reality, oreality, sempiternity, universempiternity), and it is encoded as `CONTROL_ORDER` with a strict-total-order test (HR-017). It is an order on kinds, as a prerequisite of control. A Hyperorder field is named by Tyler; this field makes no claim about it.

## Anchoring preality

[HYPOTHETICAL] Tyler's 2026-10-05 statement (in [PROVENANCE.md](PROVENANCE.md)) proposes anchoring a simulation of preality to the big bang and to the present, and running it in infinite time inside finite space. The physical picture behind it is the bubble he describes on 2026-10-04: infinite space, or finite space with infinite time.

[FRAME] Anchoring at an earlier and a later state is a two-boundary problem: fix both and ask which histories connect them. `tests/test_preality_anchor.py` is a finite toy of that, Arnold's cat map on a 60 by 60 torus with 10 by 10 blocks as macrostates:

- [FORM] Infinite time in finite space is a loop: the period is 60, so an infinite run is an exact enumeration of a finite set.
- [FORM] A micro-state has one exact past. A macro-moment has one timeline per compatible micro-state, 100 here.
- [FORM] Anchoring a second macro-moment at T=100 keeps 1 to 9 of those 100 timelines, mean 2.8 over 36 possible end macrostates.

These facts concern the toy. They do not show that any physical system behaves this way, and they do not settle three gaps: a state before the big bang needs a theory that continues past it; passage in and out of a bubble interior is not known to exist; and a backward run is exact only from a full micro-state, not from a coarse present one (HR-020).

[OPEN] Naming. Tyler's statement calls the anchored enclosure "the sempiternality" and what is accessed inside it "sempiternity". That differs from the convention above. One reading fits both, the enclosure against its interior; it is the assistant's reading and unconfirmed (HR-018). The convention stands until he confirms.

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
10. What is hypergeometric reality? It is placed in the order (2026-10-05)
    and oreality is its consequence, but no public definition exists. Its
    relation to the Hypergeometry field is also open. Is oreality around
    hypergeometric reality or within it?

11. Is the reading of "inherits upward and supports from underneath" the intended one: inherits-from pointing up, supports given by the lower kind to the higher? Which kind is the source of each?
12. What are the two unstated counterpart cells (preality temporal, base-reality atemporal), and where does areality sit in the counterpart structure?
13. Is the owner's mapping to reality classes classification only, or is there an order between kinds? What is the order, and is it on kinds or on realities?
14. Is the anchored enclosure "the sempiternality" and its interior "sempiternity", or is that a different use of the words?
15. Does "universempiternality" name the property of a universempiternity, and is the temporal sense of universempiternity unbounded?

HR-001 to HR-010 are Q1 to Q10 in [TECHNICAL_DEBT.md](TECHNICAL_DEBT.md); Q11 to Q15 are tracked as HR-013 to HR-018, and each row names its question.
