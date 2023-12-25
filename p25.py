from collections import defaultdict, deque

FNAME = "in25.txt"
    
# represent the graph in adjacency list format
graph = defaultdict(list)
for line in open(FNAME).readlines():
    names = line.replace(':','').split()
    for name in names[1:]:
        graph[names[0]].append(name)
        graph[name].append(names[0])
    
# run bfs to find a path from the source to the sink
# ignoring any edges in the banned_edges set
# returns a set of edges in the BFS path
# empty set if no such path exists
def bfs(source, sink, banned_edges):
    assert source != sink
    prev = {}
    expandQ = deque()
    expandQ.append(source)
    
    sink_found = False
    while expandQ and not sink_found:
        next_node = expandQ.popleft()
        for neighbor in graph[next_node]:
            if neighbor in prev or (neighbor, next_node) in banned_edges:
                continue
            prev[neighbor] = next_node
            if neighbor == sink:
                sink_found = True
                break
            expandQ.append(neighbor)
    
    # if we found the sink, return a set of edges (both orientations) on that path
    if sink_found:
        path_edges = set()
        current_node = sink
        while current_node != source:
            prev_node = prev[current_node]
            path_edges.add((prev_node, current_node))
            path_edges.add((current_node, prev_node))
            current_node = prev_node
        return path_edges
    
    # if the sink is unreachable, then return an empty set of removed edges
    return set()

# if there are more than three distinct BFS paths from nodeA to nodeB, 
# then they're in the same partition, 
# otherwise, they're in different partitions
# this is Edmonds Karp, more or less
def in_same_partition(nodeA, nodeB):
    banned_edges = set()
    for _ in range(3):
        new_path_edges = bfs(nodeA, nodeB, banned_edges)
        banned_edges |= new_path_edges
    new_path_edges = bfs(nodeA, nodeB, banned_edges)
    return len(new_path_edges) > 0

# arbitrarily pick the first node, 
# then check for all other nodes if they're in the same partition
all_nodes = [i for i in graph]
start_node = all_nodes[0]
a_count, b_count = 1, 0
for node in all_nodes[1:]:
    if in_same_partition(start_node, node):
        a_count += 1
    else:
        b_count += 1
print("Part 1:", a_count * b_count)
