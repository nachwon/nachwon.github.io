graph = dict()
graph['S'] = {}
graph['S']['A'] = 1
graph['S']['C'] = 2

graph['A'] = {}
graph['A']['B'] = 6

graph['B'] = {}
graph['B']['D'] = 1
graph['B']['E'] = 2

graph['C'] = {}
graph['C']['A'] = 4
graph['C']['D'] = 3

graph['D'] = {}
graph['D']['E'] = 1

graph['E'] = {}

inf = float('inf')

costs = {}

# S 에서 A 까지 도달하는데 드는 비용
costs['A'] = 1

# S 에서 C 까지 도달하는데 드는 비용
costs['C'] = 2

# 아직 비용을 알 수 없는 노드는 무한대로 설정
costs['B'] = inf
costs['D'] = inf
costs['E'] = inf

parents = {}

# A 의 부모 노드는 S
parents['A'] = 'S'

# C 의 부모 노드도 S
parents['C'] = 'S'

parents['E'] = None

processed = []

def find_lowest_cost_node(costs):
    lowest_cost = float('inf')
    lowest_cost_node = None
    for node in costs:
        cost = costs[node]
        if cost < lowest_cost and node not in processed:
            lowest_cost = cost
            lowest_cost_node = node
    return lowest_cost_node

node = find_lowest_cost_node(costs)
while node is not None:
    cost = costs[node]
    neighbors = graph[node]
    for n in neighbors.keys():
        new_cost = cost + neighbors[n]
        if costs[n] > new_cost:
            costs[n] = new_cost
            parents[n] = node
    processed.append(node)
    node = find_lowest_cost_node(costs)

def find_parents(node='E'):
    print(node)
    if node == 'S':
        return None
    parent_node = parents[node]
    return find_parents(parent_node)

find_parents()