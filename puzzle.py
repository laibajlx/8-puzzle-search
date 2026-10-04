from __future__ import division
from __future__ import print_function
import sys
import math
import time
import queue as Q
import resource

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

        # Get the index and (row, col) of empty block
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
        # for me: 
        # self.n -> 3
        # self.config -> [1,2,5,3,4,0,6,7,8]
        # self.blank_index -> 5

        if self.blank_index < self.n: #check to see if blank is alr in the top row bcuz u cant move up if alr in top row
            return None
        new_config = self.config[:]  #make copy of new board
        new_index = self.blank_index - self.n #find pos directly above the blank
        
        new_config[self.blank_index] = new_config[new_index] #swap the blank with the title above it
        new_config[new_index] = 0 

        return PuzzleState(new_config, self.n, self, "Up", self.cost + 1) #new puzzle


    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index >= self.n * (self.n - 1):  #can't move down if blank is already in the bottom row
            return None
        #make new board
        new_config = self.config[:] 
        #find pos directly below the blank and sawp with the tile below
        new_index = self.blank_index + self.n

        new_config[self.blank_index] = new_config[new_index]
        new_config[new_index] = 0

        return PuzzleState(new_config, self.n, self, "Down", self.cost + 1)


    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index % self.n == 0: 
            return None
        #make new board
        new_config = self.config[:]
        #find pos directly to the left of the blank and swap with the tile to its left
        new_index = self.blank_index - 1

        new_config[self.blank_index] = new_config[new_index] 
        new_config[new_index] = 0
        
        return PuzzleState(new_config, self.n, self, "Left", self.cost + 1)

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """

        #do the same for above except change pos index
        if self.blank_index % self.n == self.n - 1: 
            return None
        new_config = self.config[:]

        new_index = self.blank_index + 1

        new_config[self.blank_index] = new_config[new_index] 
        new_config[new_index] = 0

        return PuzzleState(new_config, self.n, self, "Right", self.cost + 1)


        

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
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children


# Function that Writes to output.txt
### Students need to change the method to have the corresponding parameters
def writeOutput():
    ### Student Code Goes here
    pass


def bfs_search(initial_state):
    """BFS search"""
    #using a queue to explore states in the order they are added -> used lecture notes
    frontier = Q.Queue()
    frontier.put(initial_state)

    explored = set()

    while not frontier.empty():
        current_state = frontier.get()

        if test_goal(current_state):
            return current_state

        explored.add(tuple(current_state.config))
        for child in current_state.expand():
            if tuple(child.config) not in explored:
                frontier.put(child)

    return None


def dfs_search(initial_state):
    """DFS search"""
    #using a stack so I explore the newest state first 
    #refer to lecture notes
    frontier = []
    frontier.append(initial_state)

    explored = set()

    while frontier:
        current_state = frontier.pop()

        if test_goal(current_state):
            return current_state

        explored.add(tuple(current_state.config))

        for child in current_state.expand():
            if tuple(child.config) not in explored:
                frontier.append(child)

    return None
    

def A_star_search(initial_state):
    """A * search"""
    # choose the state with the lowest total estimated cost
    frontier = []
    frontier.append(initial_state)

    explored = set()

    while frontier:
        current_state = min(frontier, key=calculate_total_cost)
        frontier.remove(current_state)

        if test_goal(current_state):
            return current_state

        explored.add(tuple(current_state.config))

        for child in current_state.expand():
            if tuple(child.config) not in explored:
                frontier.append(child)

    return None


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""

    #starting with the cost of reaching this state
    total_cost = state.cost

    #adding the manhattan distance of each tile
    for idx, value in enumerate(state.config):
        if value != 0:
            total_cost += calculate_manhattan_dist(idx, value, state.n)

    return total_cost

def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""

    current_row = idx // n
    current_col = idx % n

    goal_row = value // n
    goal_col = value % n

    return abs(current_row - goal_row) + abs(current_col - goal_col)


def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###
    if puzzle_state.config == list(range(puzzle_state.n * puzzle_state.n)): 
        return True
    return False


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
    print("Program completed in %.3f second(s)" % (end_time-start_time))


if __name__ == '__main__':
    main()