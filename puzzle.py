from __future__ import division
from __future__ import print_function
import sys
import math
import time
import queue as Q


#### SKELETON CODE ####

## The Class that Represents the Puzzle
class PuzzleState(object):
    """
    The PuzzleState stores a board configuration and implements
    movement instructions to generate valid children.
    """

    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g.
        [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """

        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")

        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.config = config
        self.children = []

        # Get the index of the empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[self.n*i : self.n*(i+1)])

    def move_up(self):
        """
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """

        # If blank is already in the top row, cannot move up
        if self.blank_index < self.n:
            return None

        new_config = self.config[:]

        # Find the tile above the blank
        above_index = self.blank_index - self.n

        # Swap blank and tile above it
        new_config[self.blank_index] = new_config[above_index]
        new_config[above_index] = 0

        return PuzzleState(
            new_config,
            self.n,
            self,
            "Up",
            self.cost + 1
        )

    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """

        # If blank is already in the bottom row, cannot move down
        if self.blank_index >= self.n * (self.n - 1):
            return None

        new_config = self.config[:]

        # Find the tile below the blank
        below_index = self.blank_index + self.n

        # Swap blank and tile below it
        new_config[self.blank_index] = new_config[below_index]
        new_config[below_index] = 0

        return PuzzleState(
            new_config,
            self.n,
            self,
            "Down",
            self.cost + 1
        )

    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """

        # If blank is already in the left column, cannot move left
        if self.blank_index % self.n == 0:
            return None

        new_config = self.config[:]

        # Tile to the left
        left_index = self.blank_index - 1

        # Swap blank and tile to the left
        new_config[self.blank_index] = new_config[left_index]
        new_config[left_index] = 0

        return PuzzleState(
            new_config,
            self.n,
            self,
            "Left",
            self.cost + 1
        )

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """

        # If blank is already in the right column, cannot move right
        if self.blank_index % self.n == self.n - 1:
            return None

        new_config = self.config[:]

        # Tile to the right
        right_index = self.blank_index + 1

        # Swap blank and tile to the right
        new_config[self.blank_index] = new_config[right_index]
        new_config[right_index] = 0

        return PuzzleState(
            new_config,
            self.n,
            self,
            "Right",
            self.cost + 1
        )

    def expand(self):
        """ Generate the child nodes of this node """

        # Node has already been expanded
        if len(self.children) != 0:
            return self.children

        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()
        ]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]

        return self.children


# Function that Writes to output.txt
### Students need to change the method to have the corresponding parameters
def writeOutput(goal_state, search_depth, nodes_expanded, max_fringe_size, max_search_depth, start_time):
    """
    Writes the search results to output.txt
    """

    end_time = time.time()
    running_time = end_time - start_time

    # Find the path from the goal back to the initial state
    path = []
    current = goal_state

    while current.parent is not None:
        path.append(current.action)
        current = current.parent

    # Reverse the path so it goes from start to goal
    path.reverse()

    with open("output.txt", "w") as output:
        output.write("path_to_goal: " + str(path) + "\n")
        output.write("cost_of_path: " + str(len(path)) + "\n")
        output.write("nodes_expanded: " + str(nodes_expanded) + "\n")
        output.write("search_depth: " + str(search_depth) + "\n")
        output.write("max_search_depth: " + str(max_search_depth) + "\n")
        output.write("max_fringe_size: " + str(max_fringe_size) + "\n")
        output.write("running_time: " + str(running_time) + "\n")


def bfs_search(initial_state):
    """BFS search"""

    frontier = Q.Queue()
    frontier.put(initial_state)

    explored = set()

    nodes_expanded = 0
    max_fringe_size = 1
    max_search_depth = 0

    start_time = time.time()

    while not frontier.empty():

        current = frontier.get()

        if test_goal(current):
            writeOutput(
                current,
                current.cost,
                nodes_expanded,
                max_fringe_size,
                max_search_depth,
                start_time
            )
            return current

        explored.add(tuple(current.config))

        nodes_expanded += 1

        for child in current.expand():

            if tuple(child.config) not in explored:
                frontier.put(child)

                if child.cost > max_search_depth:
                    max_search_depth = child.cost

        if frontier.qsize() > max_fringe_size:
            max_fringe_size = frontier.qsize()

    return None


def dfs_search(initial_state):
    """DFS search"""

    frontier = [initial_state]

    explored = set()

    nodes_expanded = 0
    max_fringe_size = 1
    max_search_depth = 0

    start_time = time.time()

    while len(frontier) > 0:

        current = frontier.pop()

        if test_goal(current):
            writeOutput(
                current,
                current.cost,
                nodes_expanded,
                max_fringe_size,
                max_search_depth,
                start_time
            )
            return current

        if tuple(current.config) in explored:
            continue

        explored.add(tuple(current.config))

        nodes_expanded += 1

        children = current.expand()

        # Reverse because DFS uses a stack
        children.reverse()

        for child in children:

            if tuple(child.config) not in explored:
                frontier.append(child)

                if child.cost > max_search_depth:
                    max_search_depth = child.cost

        if len(frontier) > max_fringe_size:
            max_fringe_size = len(frontier)

    return None


def A_star_search(initial_state):
    """A * search"""

    frontier = Q.PriorityQueue()

    # Each item is (total_cost, counter, state)
    counter = 0

    total_cost = calculate_total_cost(initial_state)

    frontier.put((total_cost, counter, initial_state))

    explored = set()

    nodes_expanded = 0
    max_fringe_size = 1
    max_search_depth = 0

    start_time = time.time()

    while not frontier.empty():

        total, count, current = frontier.get()

        if test_goal(current):
            writeOutput(
                current,
                current.cost,
                nodes_expanded,
                max_fringe_size,
                max_search_depth,
                start_time
            )
            return current

        if tuple(current.config) in explored:
            continue

        explored.add(tuple(current.config))

        nodes_expanded += 1

        for child in current.expand():

            if tuple(child.config) not in explored:

                counter += 1

                total_cost = calculate_total_cost(child)

                frontier.put(
                    (total_cost, counter, child)
                )

                if child.cost > max_search_depth:
                    max_search_depth = child.cost

        if frontier.qsize() > max_fringe_size:
            max_fringe_size = frontier.qsize()

    return None


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""

    # g(n) = cost from start to current state
    path_cost = state.cost

    # h(n) = Manhattan distance
    heuristic = 0

    for idx in range(len(state.config)):

        value = state.config[idx]

        # We do not calculate distance for the blank
        if value != 0:
            heuristic += calculate_manhattan_dist(
                idx,
                value,
                state.n
            )

    # f(n) = g(n) + h(n)
    return path_cost + heuristic


def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""

    # Find current row and column
    current_row = idx // n
    current_col = idx % n

    # Find goal row and column
    goal_row = value // n
    goal_col = value % n

    # Manhattan distance
    distance = abs(current_row - goal_row) + abs(current_col - goal_col)

    return distance


def test_goal(puzzle_state):
    """test the state is the goal state or not"""

    goal = list(range(puzzle_state.n * puzzle_state.n))

    return puzzle_state.config == goal


# Main Function that reads in Input and Runs corresponding Algorithm
def main():

    search_mode = sys.argv[1].lower()

    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))

    board_size = int(math.sqrt(len(begin_state)))

    hard_state = PuzzleState(begin_state, board_size)

    start_time = time.time()

    if search_mode == "bfs":
        bfs_search(hard_state)

    elif search_mode == "dfs":
        dfs_search(hard_state)

    elif search_mode == "ast":
        A_star_search(hard_state)

    else:
        print("Enter valid command arguments !")

    end_time = time.time()

    print("Program completed in %.3f second(s)" % (end_time - start_time))


if __name__ == '__main__':
    main()