graph = dict()
graph['S'] = {}
graph['S']['A'] = 2
graph['S']['B'] = 2

graph['A'] = {}
graph['A']['B'] = 2

graph['B'] = {}
graph['B']['C'] = 2
graph['B']['E'] = 25

graph['C'] = {}
graph['C']['A'] = -15
graph['C']['E'] = 2

# graph['D'] = {}
# graph['D']['E'] = 1

graph['E'] = {}

inf = float('inf')

# costs = {}

# # S 에서 A 까지 도달하는데 드는 비용
# costs['A'] = 1

# # S 에서 C 까지 도달하는데 드는 비용
# costs['C'] = 2

# 아직 비용을 알 수 없는 노드는 무한대로 설정

parents = {}

# A 의 부모 노드는 S
parents['A'] = 'S'

# C 의 부모 노드도 S
parents['B'] = 'S'

parents['E'] = None

processed = []

def set_costs_table(graph, start='S'):
    costs = {}
    costs = graph['S']
    for i, j in graph.items():
        if i not in graph['S'] and i != 'S':
            costs[i] = float('inf')
    return costs

costs = set_costs_table(graph, 'S')

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

print(set_costs_table(graph))
print(costs)