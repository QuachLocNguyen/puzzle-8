import heapq
import copy
import streamlit as st

class PuzzleState:
    def __init__(self, board, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move
        self.g = 0  # Cost from start node
        self.h = self.calculate_heuristic()  # Estimated cost to goal
        self.f = self.g + self.h  # Total estimated cost

    def __lt__(self, other):
        # Allows comparison for priority queue
        return self.f < other.f

    def calculate_heuristic(self):
        # Manhattan distance heuristic
        goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        distance = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 0:
                    goal_pos = self.find_position(goal, self.board[i][j])
                    distance += abs(i - goal_pos[0]) + abs(j - goal_pos[1])
        return distance

    def find_position(self, board, value):
        for i in range(3):
            for j in range(3):
                if board[i][j] == value:
                    return (i, j)
        return None

    def is_goal(self):
        goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        return self.board == goal

    def get_neighbors(self):
        neighbors = []
        zero_pos = self.find_position(self.board, 0)
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up

        for dx, dy in moves:
            new_x, new_y = zero_pos[0] + dx, zero_pos[1] + dy
            
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_board = copy.deepcopy(self.board)
                # Swap zero with adjacent tile
                new_board[zero_pos[0]][zero_pos[1]], new_board[new_x][new_y] = \
                new_board[new_x][new_y], new_board[zero_pos[0]][zero_pos[1]]
                
                neighbor = PuzzleState(new_board, self, (dx, dy))
                neighbor.g = self.g + 1
                neighbor.f = neighbor.g + neighbor.h
                neighbors.append(neighbor)
        
        return neighbors

def a_star_search(initial_state):
    frontier = []
    heapq.heappush(frontier, initial_state)
    explored = set()

    while frontier:
        current = heapq.heappop(frontier)

        # Convert board to tuple for hashable comparison
        board_tuple = tuple(tuple(row) for row in current.board)
        if board_tuple in explored:
            continue

        explored.add(board_tuple)

        if current.is_goal():
            # Reconstruct path
            path = []
            while current:
                path.append(current.board)
                current = current.parent
            return list(reversed(path))

        for neighbor in current.get_neighbors():
            heapq.heappush(frontier, neighbor)

    return None

def solve_8_puzzle(initial_board):
    initial_state = PuzzleState(initial_board)
    solution = a_star_search(initial_state)
    return solution

def display_board(board):
    board_str = ""
    for row in board:
        board_str += " ".join(str(x) if x != 0 else " " for x in row) + "\n"
    return board_str

def main():
    st.title("8-Puzzle Solver")
    
    # Input initial board configuration
    st.write("Enter the initial board configuration (use 0 for empty space):")
    board_input = []
    for i in range(3):
        row = [
            st.number_input(f"Row {i+1}, Column 1", min_value=0, max_value=8, key=f"row{i}col0"),
            st.number_input(f"Row {i+1}, Column 2", min_value=0, max_value=8, key=f"row{i}col1"),
            st.number_input(f"Row {i+1}, Column 3", min_value=0, max_value=8, key=f"row{i}col2")
        ]
        board_input.append(row)

    if st.button("Solve Puzzle"):
        # Validate input
        if len(set([num for row in board_input for num in row])) != 9:
            st.error("Please ensure each number (0-8) is used exactly once.")
            return

        solution = solve_8_puzzle(board_input)

        if solution:
            st.write(f"Solution found in {len(solution) - 1} moves!")
            for i, board in enumerate(solution):
                st.text(f"Step {i}:")
                st.text(display_board(board))
        else:
            st.write("No solution exists for this puzzle configuration.")

if __name__ == "__main__":
    main()
