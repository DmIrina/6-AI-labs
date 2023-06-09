import random
import time
from queue import PriorityQueue


# Клас для представлення стану дошки з ферзями
class BoardState:
    node_count = 0  # Лічильник кількості сгенерованих вузлів
    max_nodes = 0  # Лічильник максимальної кількості вузлів, що зберігаються в пам'яті

    def __init__(self, queens, cost):
        self.queens = queens  # розміщення ферзів на дошці
        self.cost = cost  # вартість поточного стану
        self.res = [""] * 8

    # Метод для перевірки, чи є конфлікти між ферзями
    def is_conflict(self, row, col):
        for queen in self.queens:
            q_row, q_col = queen
            if q_row == row or q_col == col or abs(q_row - row) == abs(q_col - col):
                return True
        return False

    # Метод для визначення нового стану після розміщення ферзя
    def next_state(self, row, col):
        queens = self.queens.copy()
        queens.append((row, col))
        cost = self.cost + 1
        return BoardState(queens, cost)

    # Метод для виведення стану дошки
    def print_board(self, elapsed_time):
        for i in range(8):
            for j in range(8):
                if (i, j) in self.queens:
                    print("Q", end=" ")
                    self.res[j] = str(i + 1)
                else:
                    print(".", end=" ")
            print()
        print()
        print("".join(self.res) + "  %.3f " % elapsed_time, BoardState.node_count, BoardState.max_nodes)




    # Методи для порівняння станів дошки для використання в пріоритетній черзі
    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.queens == other.queens


# Функція, яка вирішує задачу 8-ферзів з використанням UCS
def solve_eight_queens():
    # Виклик функції для вирішення задачі з вимірюванням часу виконання
    start_time = time.time()

    start_queens = []
    col_placement = random.randint(0, 7)
    start_queens.append((0, col_placement))  # Випадкове розміщення ферзя у першому рядку

    start_state = BoardState(start_queens, 0)

    queue = PriorityQueue()
    queue.put(start_state)

    while not queue.empty():
        current_state = queue.get()

        # Якщо дошка заповнена, виводимо розв'язок і завершуємо виконання
        if len(current_state.queens) == 8:
            elapsed_time = time.time() - start_time
            current_state.print_board(elapsed_time)
            return

        # Розміщуємо ферзя на наступний рядок
        next_row = len(current_state.queens)
        for col in range(8):
            if not current_state.is_conflict(next_row, col):
                next_state = current_state.next_state(next_row, col)
                queue.put(next_state)
                BoardState.node_count += 1
                BoardState.max_nodes = max(BoardState.max_nodes, queue.qsize())

    print("Розв'язок не знайдено.")
    print("Максимальна кількість вузлів, що зберігаються в пам'яті:", BoardState.max_nodes)



solve_eight_queens()




