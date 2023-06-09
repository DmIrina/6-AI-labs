from queue import PriorityQueue


class Node:
    def __init__(self, state, parent=None, g=0):
        self.state = state
        self.parent = parent
        self.g = g  # cost from start node to current node

    def __lt__(self, other):
        return self.g < other.g


def count_attacking_pairs(state):
    n = len(state)
    attacking_pairs = 0

    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j]:  # same column
                attacking_pairs += 1
            elif abs(state[i] - state[j]) == abs(i - j):  # diagonal attack
                attacking_pairs += 1

    return attacking_pairs


def generate_neighbors(node):
    neighbors = []
    n = len(node.state)
    for col in range(n):
        for row in range(n):
            if node.state[col] != row:
                neighbor_state = list(node.state)
                neighbor_state[col] = row
                neighbor = Node(neighbor_state, parent=node, g=node.g + 1)
                neighbors.append(neighbor)
    return neighbors


def ucs_search(start_state):
    max_explored_nodes = 0
    max_stored_nodes = 0

    start_node = Node(start_state, g=0)
    open_set = PriorityQueue()
    open_set.put(start_node)
    closed_set = set()

    while not open_set.empty():
        max_stored_nodes = max(max_stored_nodes, open_set.qsize() + len(closed_set))
        current_node = open_set.get()

        if count_attacking_pairs(current_node.state) == 0:
            solution = []
            while current_node:
                solution.append(current_node.state)
                current_node = current_node.parent
            solution.reverse()
            print("Максимальна кількість вузлів, що відвідані:", max_explored_nodes)
            print("Максимальна кількість вузлів, що зберігаються в пам'яті:", max_stored_nodes)
            return solution

        closed_set.add(tuple(current_node.state))
        max_explored_nodes = max(max_explored_nodes, len(closed_set))

        neighbors = generate_neighbors(current_node)
        for neighbor in neighbors:
            if tuple(neighbor.state) in closed_set:
                continue
            if neighbor not in open_set.queue:
                open_set.put(neighbor)
            else:
                # Update the cost if a better path is found
                for item in open_set.queue:
                    if item == neighbor and item.g > neighbor.g:
                        open_set.queue.remove(item)
                        open_set.put(neighbor)

    return None


def print_solution(solution):
    n = len(solution[0])
    for state in solution:
        print("-" * (2 * n + 1))
        for row in range(n):
            line = "|"
            for col in range(n):
                if state[col] == row:
                    line += " Q |"
                else:
                    line += "   |"
            print(line)
    print("-" * (2 * n + 1))


# Вхідні дані - початковий стан дошки
start_state = [0, 0, 0, 0, 0, 0, 0, 0]

# Запуск алгоритму UCS
solution = ucs_search(start_state)

# Виведення розв'язку у вигляді матриці
if solution is None:
    print("Розв'язок не знайдено.")
else:
    print("Розв'язок знайдено:")
    print_solution(solution)
