"""Finite frame for what a reality is and which kinds of reality are declared.

This module states kinds, presentations of those kinds, and two relations that
are kept apart: classification (is-a) and containment (is-in). It does not
rank kinds, does not alias one kind name to another, does not decide whether
containment runs from sempiternity to reality or the other way, and does not
define observability (that is Hyperspace's subject).
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
    """A declared kind of reality. Kinds are unordered: comparing two raises."""
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
class Registry:
    kinds: tuple
    presentations: tuple
    wholes: tuple = ()
    classifications: tuple = ()
    containments: tuple = ()

    def __post_init__(self) -> None:
        _bounded(self.kinds, Kind, "kinds")
        _bounded(self.presentations, Presentation, "presentations")
        _bounded(self.wholes, Whole, "wholes")
        _bounded(self.classifications, Classification, "classifications")
        _bounded(self.containments, Containment, "containments")
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
    Kind("areality", "abstract artificial reality; where thought, as a projection of a "
         "constructed reality, is placed", "USER-STATED 2026-09-21; see PROVENANCE.md"),
    Kind("surreality", "the dream reality", "USER-STATED 2026-09-21; see PROVENANCE.md"),
    Kind("preality", "possibility reality", "USER-STATED 2026-09-21; see PROVENANCE.md"),
    Kind("oreality", "springs out from areality", "USER-STATED 2026-09-23; "
         "metamathethicology commit 846ce08; see PROVENANCE.md"),
    Kind("hypergeometric-reality", "proposed further kind; not yet defined here",
         "USER-PROPOSED as recorded in hyperobjectivity ed75d14 and "
         "hypersubjectivity 1f7f8a7; see PROVENANCE.md"),
)
