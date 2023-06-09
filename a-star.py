import time
import random

class Node:
    max_explored_nodes = 0
    max_stored_nodes = 0

    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.g = g  # cost from start node to current node
        self.h = h  # heuristic value (F1) from current node to goal

    def f(self):
        return self.g + self.h


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


def a_star_search(start_state):
    Node.max_explored_nodes = 0
    Node.max_stored_nodes = 0

    start_node = Node(start_state, g=0, h=count_attacking_pairs(start_state))
    open_set = [start_node]
    closed_set = set()

    while open_set:
        Node.max_stored_nodes = max(Node.max_stored_nodes, len(open_set) + len(closed_set))
        current_node = min(open_set, key=lambda node: node.f())
        open_set.remove(current_node)

        if count_attacking_pairs(current_node.state) == 0:
            solution = []
            while current_node:
                solution.append(current_node.state)
                current_node = current_node.parent
            solution.reverse()
            return solution

        closed_set.add(tuple(current_node.state))
        Node.max_explored_nodes = max(Node.max_explored_nodes, len(closed_set))

        neighbors = generate_neighbors(current_node)
        for neighbor in neighbors:
            if tuple(neighbor.state) in closed_set:
                continue
            if neighbor not in open_set:
                neighbor.h = count_attacking_pairs(neighbor.state)
                open_set.append(neighbor)

    return None


def print_solution(solution, elapsed_time):
    n = len(solution[0])
    m = len(solution)
    state = solution[m - 1]
    res = [""] * n
    for row in range(n):
        line = ""
        res[row] = str(state[row] + 1)
        for col in range(n):
            if state[col] == row:
                line += "Q "
            else:
                line += ". "
        print(line)
    print("".join(res) + "  %.3f " % elapsed_time, Node.max_explored_nodes, Node.max_stored_nodes)



# Генерування випадкового початкового стану
n = 8  # Розмірність шахової дошки
start_state = [random.randint(0, n - 1) for _ in range(n)]

# Запуск алгоритму A-Star з вимірюванням часу
start_time = time.time()
solution = a_star_search(start_state)
elapsed_time = time.time() - start_time

# Виведення розв'язку та часу виконання
if solution is None:
    print("Розв'язок не знайдено.")
else:
    print("Розв'язок знайдено:")
    print_solution(solution, elapsed_time)
