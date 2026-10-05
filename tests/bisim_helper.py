"""Shared finite helper for the bisimulation tests; not a test module.

Containment is read as a directed graph: an edge (a, b) means "a contains b".
Two nodes are bisimilar when they fall in the same block of the coarsest
partition in which equivalent nodes have the same set of successor blocks
(partition refinement). The helper is bounded by the size of its input and
always terminates: each round either splits a block or stops.
"""


def bisimulation_classes(nodes, edges):
    """Return {node: block id} for the coarsest bisimulation partition."""
    nodes = list(nodes)
    successors = {n: set() for n in nodes}
    for a, b in edges:
        if a not in successors or b not in successors:
            raise ValueError(f"edge ({a!r}, {b!r}) names an unknown node")
        successors[a].add(b)
    block = {n: 0 for n in nodes}
    while True:
        signature = {n: (block[n], frozenset(block[m] for m in successors[n]))
                     for n in nodes}
        ids = {}
        refined = {n: ids.setdefault(signature[n], len(ids)) for n in nodes}
        if len(set(refined.values())) == len(set(block.values())):
            return refined
        block = refined


def containment_graph(reg):
    """Nodes and (container, member) edges of a hyperreality Registry."""
    nodes = sorted({p.reality_id for p in reg.presentations}
                   | {w.whole_id for w in reg.wholes})
    return nodes, [(c.container_id, c.member_id) for c in reg.containments]
