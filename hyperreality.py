"""Finite frame for what a reality is and which kinds of reality are declared.

This module states kinds, presentations of those kinds, and two relations that
are kept apart: classification (is-a) and containment (is-in). It also declares
the owner's control order of the kinds (USER-STATED 2026-10-05): each layer is
reached by first gaining control of the layers below it. That order is an
explicit declaration, not Python ordering on Kind: comparing two Kind objects
still raises, and the order says nothing about "more real". The module does not
alias one kind name to another, does not decide whether containment runs from
sempiternity to reality or the other way, and does not define observability
(that is Hyperspace's subject).
"""

from dataclasses import dataclass
import re

_TOKEN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
MAX_ITEMS = 256


def _token(value: object, what: str) -> str:
    if not isinstance(value, str) or not _TOKEN.fullmatch(value):
        raise ValueError(f"{what} must be a 1-64 character token, got {value!r}")
    return value


def _text(value: object, what: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 512:
        raise ValueError(f"{what} must be non-empty text of at most 512 characters")
    return value


def _bounded(items: object, cls: type, what: str) -> tuple:
    if not isinstance(items, tuple):
        raise ValueError(f"{what} must be a tuple")
    if len(items) > MAX_ITEMS:
        raise ValueError(f"{what} exceeds {MAX_ITEMS} entries")
    for item in items:
        if not isinstance(item, cls):
            raise ValueError(f"{what} entries must be {cls.__name__}")
    return items


@dataclass(frozen=True)
class Kind:
    """A declared kind of reality. Comparing two Kind objects raises; the order is CONTROL_ORDER."""
    name: str
    gloss: str
    source: str

    def __post_init__(self) -> None:
        _token(self.name, "kind name")
        _text(self.gloss, "kind gloss")
        _text(self.source, "kind source")


@dataclass(frozen=True)
class Presentation:
    """One reality instance presented as exactly one declared kind."""
    reality_id: str
    kind: str

    def __post_init__(self) -> None:
        _token(self.reality_id, "reality id")
        _token(self.kind, "kind")


@dataclass(frozen=True)
class Whole:
    """An instance of a class that is not itself a declared kind, such as a
    sempiternity (an instance of the class sempiternality) used as a container."""
    whole_id: str
    class_name: str

    def __post_init__(self) -> None:
        _token(self.whole_id, "whole id")
        _token(self.class_name, "class name")


@dataclass(frozen=True)
class Classification:
    """member is-a class_name. Says nothing about where member is."""
    member_id: str
    class_name: str

    def __post_init__(self) -> None:
        _token(self.member_id, "member id")
        _token(self.class_name, "class name")


@dataclass(frozen=True)
class Containment:
    """member is-in container. Says nothing about what member is."""
    container_id: str
    member_id: str

    def __post_init__(self) -> None:
        _token(self.container_id, "container id")
        _token(self.member_id, "member id")
        if self.container_id == self.member_id:
            raise ValueError("an identity does not directly contain itself")


@dataclass(frozen=True)
class Counterpart:
    """temporal_id and atemporal_id present the same kind of reality, one with and one
    without a time of its own. A third relation, never read as is-a or is-in (HR-014)."""
    temporal_id: str
    atemporal_id: str

    def __post_init__(self) -> None:
        _token(self.temporal_id, "temporal id")
        _token(self.atemporal_id, "atemporal id")
        if self.temporal_id == self.atemporal_id:
            raise ValueError("an identity is not its own counterpart")


@dataclass(frozen=True)
class Registry:
    kinds: tuple
    presentations: tuple
    wholes: tuple = ()
    classifications: tuple = ()
    containments: tuple = ()
    counterparts: tuple = ()

    def __post_init__(self) -> None:
        _bounded(self.kinds, Kind, "kinds")
        _bounded(self.presentations, Presentation, "presentations")
        _bounded(self.wholes, Whole, "wholes")
        _bounded(self.classifications, Classification, "classifications")
        _bounded(self.containments, Containment, "containments")
        _bounded(self.counterparts, Counterpart, "counterparts")
        names = [k.name for k in self.kinds]
        if len(names) != len(set(names)):
            raise ValueError("kind names must be distinct")
        for p in self.presentations:
            if p.kind not in names:
                raise ValueError(f"undeclared kind {p.kind!r}; kinds are never aliased")
        ids = [p.reality_id for p in self.presentations] + [w.whole_id for w in self.wholes]
        if len(ids) != len(set(ids)):
            raise ValueError("reality and whole identities must be distinct")
        known = set(ids)
        for c in self.classifications:
            if c.member_id not in known:
                raise ValueError(f"classification names unknown member {c.member_id!r}")
        for c in self.containments:
            if c.container_id not in known or c.member_id not in known:
                raise ValueError("containment endpoints must be declared identities")
        if len(set(self.classifications)) != len(self.classifications):
            raise ValueError("classifications must not repeat")
        if len(set(self.containments)) != len(self.containments):
            raise ValueError("containments must not repeat")
        kind_of = {p.reality_id: p.kind for p in self.presentations}
        for c in self.counterparts:
            for end in (c.temporal_id, c.atemporal_id):
                if end not in kind_of:
                    raise ValueError(f"counterpart endpoint {end!r} must be a presented reality")
            if kind_of[c.temporal_id] != kind_of[c.atemporal_id]:
                raise ValueError("counterparts present the same kind of reality")
        if len({c.temporal_id for c in self.counterparts}) != len(self.counterparts):
            raise ValueError("a reality has at most one atemporal counterpart")
        if len({c.atemporal_id for c in self.counterparts}) != len(self.counterparts):
            raise ValueError("a reality is the atemporal counterpart of at most one reality")


def resolve_kind(reg: Registry, name: str) -> Kind:
    """Exact name match only; there is no fallback and no alias table."""
    for kind in reg.kinds:
        if kind.name == name:
            return kind
    raise KeyError(name)


def instances_of_kind(reg: Registry, name: str) -> frozenset:
    """Every presentation of a kind. Uniqueness of any kind is not assumed."""
    resolve_kind(reg, name)
    return frozenset(p.reality_id for p in reg.presentations if p.kind == name)


def classes_of(reg: Registry, identity: str) -> frozenset:
    """Directly declared classifications only; containment is not consulted."""
    return frozenset(c.class_name for c in reg.classifications if c.member_id == identity)


def _closure(reg: Registry, start: str, upward: bool) -> frozenset:
    step = {}
    for c in reg.containments:
        a, b = (c.member_id, c.container_id) if upward else (c.container_id, c.member_id)
        step.setdefault(a, []).append(b)
    seen, frontier = set(), [start]
    while frontier:
        for nxt in step.get(frontier.pop(), ()):
            if nxt not in seen:
                seen.add(nxt)
                frontier.append(nxt)
    return frozenset(seen)


def containers_of(reg: Registry, identity: str) -> frozenset:
    """Everything that transitively contains identity. Classification is not consulted."""
    return _closure(reg, identity, upward=True)


def members_of(reg: Registry, identity: str) -> frozenset:
    """Everything identity transitively contains. Classification is not consulted."""
    return _closure(reg, identity, upward=False)


def well_founded(reg: Registry) -> bool:
    """True when no identity transitively contains itself. This is reported,
    not enforced: a registry in which containment loops is representable."""
    ids = {p.reality_id for p in reg.presentations} | {w.whole_id for w in reg.wholes}
    return all(i not in containers_of(reg, i) for i in ids)


DECLARED_KINDS = (
    Kind("base-reality", "N-d universal base reality",
         "USER-STATED 2026-09-21; see PROVENANCE.md"),
    Kind("surreality", "the dream reality; dream control, e.g. lucid and controllable "
         "dreamscapes", "USER-STATED 2026-09-21 and 2026-10-05; see PROVENANCE.md"),
    Kind("areality", "abstract artificial reality, unobservably indifferent from base "
         "reality, entered by mind linking (conscious, through apparatus, or "
         "asynchronous, by upload); where thought, as a projection of a constructed "
         "reality, is placed", "USER-STATED 2026-09-21 and 2026-10-05; see PROVENANCE.md"),
    Kind("preality", "possibility reality; arises only when we try to link into our own "
         "reality, through which unobservable natural laws are learned",
         "USER-STATED 2026-09-21 and 2026-10-05; see PROVENANCE.md"),
    Kind("hypergeometric-reality", "the hypergeometric reality; its existence has oreality "
         "as a consequence", "USER-PROPOSED as recorded in hyperobjectivity ed75d14 and "
         "hypersubjectivity 1f7f8a7; placed in the order USER-STATED 2026-10-05"),
    Kind("oreality", "the transfinite-dimensional reality that naturally exists as a "
         "consequence of the hypergeometric reality existing; around or within it",
         "USER-STATED 2026-09-23 (metamathethicology commit 846ce08) and 2026-10-05; "
         "see PROVENANCE.md"),
    Kind("sempiternity", "the object that holds sempiternality; unbounded in time",
         "USER-STATED 2026-09-26 and 2026-10-05; see PROVENANCE.md, Naming"),
    Kind("universempiternity", "the superstructure of sempiternity: contains all kinds "
         "below it, sempiternity, and itself", "USER-STATED 2026-10-04 and 2026-10-05; "
         "see PROVENANCE.md, Naming"),
)

# The owner's order, lowest first (USER-STATED 2026-10-05). With each layer one must
# first gain control of the layers below it. "Around or within" for oreality is open.
CONTROL_ORDER = ("base-reality", "surreality", "areality", "preality",
                 "hypergeometric-reality", "oreality", "sempiternity",
                 "universempiternity")


def control_position(name: str) -> int:
    """Index of a kind in CONTROL_ORDER (0 is base-reality). KeyError if unplaced."""
    try:
        return CONTROL_ORDER.index(name)
    except ValueError:
        raise KeyError(f"kind {name!r} has no place in the control order") from None


def control_prerequisites(name: str) -> tuple:
    """Kinds whose control must be gained before this one, lowest first."""
    return CONTROL_ORDER[:control_position(name)]


def controlled_before(lower: str, higher: str) -> bool:
    """True when control of `lower` is a prerequisite of reaching `higher`."""
    return control_position(lower) < control_position(higher)


def order_is_declared(kinds=DECLARED_KINDS) -> bool:
    """True when CONTROL_ORDER lists every declared kind exactly once."""
    names = [k.name for k in kinds]
    return sorted(names) == sorted(CONTROL_ORDER) and len(set(CONTROL_ORDER)) == len(CONTROL_ORDER)


# --- Counterparts, simulation and access (USER-STATED 2026-10-05 and 2026-10-06) -----------

# Kinds the owner says have an atemporal counterpart: surreality, preality, base-reality
# (2026-10-05) and areality (2026-10-06, "atemporal versions of base-reality, areality, ...").
# Hypergeometric reality and oreality are covered only by the "...", so they are not listed.
KINDS_WITH_ATEMPORAL_COUNTERPART = ("base-reality", "surreality", "areality", "preality")

# Kinds the owner says an areality device can simulate: all lower orders than sempiternity.
# Representation is not control: this is a different relation from CONTROL_ORDER.
SIMULABLE_IN_AREALITY = CONTROL_ORDER[:control_position("sempiternity")]

# Kinds obtainable from preality simulations (2026-10-06): base-reality, and surreality as
# the accessible imagination spaces of each simulated law-abiding universe.
OBTAINABLE_FROM_PREALITY = ("base-reality", "surreality")


def areality_can_simulate(kind: str) -> bool:
    """True for every kind below sempiternity in CONTROL_ORDER, including areality itself.
    Sempiternity and above are not simulated; access to sempiternity is by a nulltime
    device (2026-10-06). KeyError for a kind with no place in the order."""
    control_position(kind)
    return kind in SIMULABLE_IN_AREALITY


def atemporal_of(reg: Registry, identity: str):
    """The declared atemporal counterpart of identity, or None. Nothing is inferred."""
    for c in reg.counterparts:
        if c.temporal_id == identity:
            return c.atemporal_id
    return None


def temporal_of(reg: Registry, identity: str):
    """The declared temporal counterpart of identity, or None."""
    for c in reg.counterparts:
        if c.atemporal_id == identity:
            return c.temporal_id
    return None


def counterpart_law_violations(reg: Registry) -> tuple:
    """The preality law of 2026-10-06: atemporal versions of the listed kinds exist for
    every reality of those kinds, and they lie within a sempiternity (the nullspace is
    technically sempiternity). Returns (reality_id, reason) pairs; empty means the law holds
    in this registry. Reported, not enforced: a registry that violates it is representable."""
    sempiternities = {w.whole_id for w in reg.wholes if w.class_name == "sempiternality"}
    out = []
    for p in reg.presentations:
        if p.kind not in KINDS_WITH_ATEMPORAL_COUNTERPART:
            continue
        if temporal_of(reg, p.reality_id) is not None:
            continue  # it is itself an atemporal counterpart
        twin = atemporal_of(reg, p.reality_id)
        if twin is None:
            out.append((p.reality_id, "no atemporal counterpart"))
        elif not (containers_of(reg, twin) & sempiternities):
            out.append((p.reality_id, "atemporal counterpart is not within a sempiternity"))
    return tuple(out)
