from __future__ import annotations

'''
    A vertex corresponding to a map Node that can be
    rendered to the screen and holds some metadata
'''
class DebugVertex:
    def __init__(self, x: float, y: float, name: str, node: Node):
        self.coords = [x,y]
        self.node = node
        self.name = name

'''
    A map node that can connect to other map nodes
'''
class Node:
    def __init__(self, name: str):
        self.name = name
        self.connected = [] # (Node, Distance)
        self.from_start = 0
        self.prev: Node | None = None
        # gui interaction
        self.gui_inter: DebugVertex = DebugVertex(0.0, 0.0, "null", self)

    ''' Join two nodes and state their distance '''
    def connect(self, node: Node, dist: float):
        self.connected.append((node, dist))
        node.connected.append((self, dist))

'''
    Find a path from start to end, updating the nodes
    passed to point a path back to start.
    returns the final node if it's found, or a null node
    if it could not be
'''
def traverse_node(start: Node, end: Node) -> Node:
    been = []
    at = [start]
    going = []
    while len(at) > 0:
        node = at[0]
        for (possibility, dist) in node.connected:
            real_dist = dist + node.from_start
            if possibility == end:
                end.prev = node
                end.from_start = real_dist
                return end
            if (possibility.from_start == 0 or possibility.from_start > real_dist) and possibility not in been and possibility not in at:
                possibility.from_start = real_dist
                possibility.prev = node
                going.append(possibility)
        been.append(node)
        at.remove(node)
        at += going
        going = []
    return Node("null")

'''
    An alternative traverse function that isn't as good as traverse_node
'''
def alt_traverse_node(start: Node, end: Node) -> Node:
    been = []
    at = [start]
    going = []
    while True:
        for node in at:
            for (neighbor, weight) in node.connected:
                if neighbor == end:
                    neighbor.prev = node
                    return neighbor
                if not neighbor in at and not neighbor in been:
                    neighbor.from_start = weight
                    neighbor.prev = node
                    going.append(neighbor)
                    continue
        been += at
        at = going
        going = []

'''
    Reverse the steps taken in traverse_nodes to create a path
'''
def reverse_traversal(start: Node, end: Node) -> list[Node]:
    nodes = []
    current = end
    while current != start and current != None:
        nodes.append(current)
        current = current.prev
    nodes.append(start)
    return nodes

''' Manual testing '''
if __name__ == '__main__':
    blair = Node('blair')
    chancellor = Node("chancellor")
    tucker = Node("Tucker")
    wren = Node("wren")
    ewell = Node("ewell")
    washington = Node("washington")
    mcglothlin = Node("Mcglothlin")
    meadow = Node("meadow")

    blair.connect(chancellor, 1)
    blair.connect(meadow, 1)
    blair.connect(mcglothlin, 1)

    meadow.connect(mcglothlin, 1)

    mcglothlin.connect(washington, 1)

    washington.connect(chancellor, 1)
    washington.connect(ewell, 1)

    tucker.connect(chancellor, 1)
    tucker.connect(ewell, 1)
    tucker.connect(wren, 1)

    wren.connect(ewell, 1)

    path = reverse_traversal(meadow, traverse_node(meadow, wren))
    for p in path:
        print(p.name)
