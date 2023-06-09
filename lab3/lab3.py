# This is a sample Python script.
from random import random, choice

import numpy as np
from matplotlib import pyplot as plt


class ValueIterationAgent:
    def __init__(self, environment):
        self.environment = environment
        self.V = np.zeros_like(self.environment.grid)  # Value function
        self.discount_factor = 0.9
        self.path = []  # List to store the path
        self.rewards = []  # List to store the rewards

    def value_iteration2(self):
        iter_num = 0
        delta = 0

        while True:
            V_new = np.copy(self.V)
            delta = 0

            for state in self.environment.get_all_states():
                if state in self.environment.terminal_states or state in self.environment.obstacles:
                    self.V[state] = self.environment.get_reward(state)
                    V_new[state] = self.environment.get_reward(state)
                    continue

                action_values = []

                for action in self.environment.get_available_actions(state):
                    next_state = self.environment.get_next_state(state, action)
                    value = self.environment.get_reward(state) + self.discount_factor * self.V[next_state]
                    action_values.append(value)

                max_value = max(action_values)
                delta = max(delta, abs(max_value - self.V[state]))
                V_new[state] = max_value

            self.V = V_new

            if delta < 1e-2:
                break

            iter_num += 1
            print(f"iter_num: {iter_num}")
            np.set_printoptions(formatter={'float': lambda x: "{0:0.01f}".format(x)})
            # print(self.V)
        print(f"we completed value iteration at {iter_num} iterations")
        return iter_num


class GridWorld:
    ## Initialise starting data
    def __init__(self, num_rooms):
        # Set information about the gridworld
        self.height = 50
        self.width = 50

        self.grid = np.zeros((self.height, self.width)) - 1
        # Set random start location for the agent
        self.current_location = (7, np.random.randint(0, 5))

        # Set locations for the bomb and the gold
        # self.bomb_location = (np.random.randint(0,self.width), np.random.randint(0,self.height))
        # self.gold_location = (np.random.randint(0,self.width), np.random.randint(0,self.height))
        #
        #

        self.bomb_location = (6, 6)
        self.gold_location = (1, self.width - 2)

        self.terminal_states = [self.bomb_location, self.gold_location]
        self.obstacles = []

        # Set available actions
        self.actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        room_size = 4

        gold_num = 0
        gold_req = int(num_rooms / 5)

        start_x = 1
        start_y = 1

        cur_room_num = 0
        # loop intil we haven't build num_rooms
        bombs_num = 0
        bombs_req = int(num_rooms / 3)
        while cur_room_num < num_rooms:

            door = choice(["bottom", "top", "left", "right"])

            self.add_rooms((start_x, start_y), (room_size, room_size), door)
            # put a bomb in the room with prob 0.2
            if bombs_num < bombs_req and random() < 0.5:
                self.bomb_location = (start_x + 1, start_y + 1)
                self.terminal_states.append(self.bomb_location)
                self.grid[self.bomb_location[0], self.bomb_location[1]] = -100
                print("bomb location: ", self.bomb_location)
                bombs_num = bombs_num + 1
            else:
                if gold_num < gold_req:
                    self.gold_location = (start_x + 1, start_y + 1)
                    self.terminal_states.append(self.gold_location)
                    self.grid[self.gold_location[0], self.gold_location[1]] = 100
                    print("gold location: ", self.gold_location)
                    gold_num = gold_num + 1

            start_x = start_x + room_size + 1
            if start_x > self.height - room_size:
                start_x = 1
                start_y = start_y + room_size + 1

            cur_room_num += 1

        # Set grid rewards for special cells
        self.grid[self.bomb_location[0], self.bomb_location[1]] = -100
        self.grid[self.gold_location[0], self.gold_location[1]] = 100
        print(self.grid)

    def get_available_actions(self, state):
        """Returns possible actions considering the walls."""
        actions = []
        current_location = state

        if current_location[0] > 0 and not self.check_walls((current_location[0] - 1, current_location[1])):
            actions.append('UP')

        if current_location[0] < self.height - 1 and not self.check_walls(
                (current_location[0] + 1, current_location[1])):
            actions.append('DOWN')

        if current_location[1] > 0 and not self.check_walls((current_location[0], current_location[1] - 1)):
            actions.append('LEFT')

        if current_location[1] < self.width - 1 and not self.check_walls(
                (current_location[0], current_location[1] + 1)):
            actions.append('RIGHT')

        return actions

    def get_all_states(self):
        """Returns a list of all possible states in the gridworld."""
        states = []
        for i in range(self.height):
            for j in range(self.width):
                states.append((i, j))
        return states

    def get_next_state(self, state, action, slipping_prob=0):
        """Returns the next state given the current state and chosen action."""
        float_r = random()
        if float_r < slipping_prob:
            # Slipping occurs, choose a random action instead
            action = choice(self.get_available_actions(state))

        if action == 'UP':
            next_state = (state[0] - 1, state[1])
        elif action == 'DOWN':
            next_state = (state[0] + 1, state[1])
        elif action == 'LEFT':
            next_state = (state[0], state[1] - 1)
        elif action == 'RIGHT':
            next_state = (state[0], state[1] + 1)
        else:
            next_state = state

        # Check if the next state is valid (not hitting a wall or going out of bounds)
        if next_state[0] < 0 or next_state[0] >= self.height or next_state[1] < 0 or next_state[1] >= self.width:
            next_state = state

        return next_state

    def check_walls(self, location):
        """Check if the agent is trying to cross a wall.

        Args:
            location (tuple): Current location of the agent.

        Returns:
            bool: True if there is a wall, False otherwise.
        """
        if location in self.obstacles:
            return True
        else:
            return False

    ### Add rooms and blockages
    def add_rooms(self, room_location, room_size, door_position):
        """Add a rectangular room with specified location and size to the grid"""
        for i in range(room_location[0], room_location[0] + room_size[0]):
            for j in range(room_location[1], room_location[1] + room_size[1]):
                if i == room_location[0] or i == room_location[0] + room_size[0] - 1 or j == room_location[1] or j == \
                        room_location[1] + room_size[1] - 1:
                    self.grid[i, j] = None
                    self.obstacles.append((i, j))
                else:
                    self.grid[i, j] = -1

        # add a hole in the wall as door in the center of one of the walls of the room
        if door_position == "bottom":
            # add a hole in the wall as door in the center of right wall of the room
            self.grid[room_location[0] + room_size[0] - 1, room_location[1] + int(room_size[0] / 2)] = -1
            self.obstacles.remove((room_location[0] + room_size[0] - 1, room_location[1] + int(room_size[0] / 2)))
        elif door_position == "left":
            self.grid[room_location[0] + int(room_size[0] / 2), room_location[1]] = -1
            self.obstacles.remove((room_location[0] + int(room_size[0] / 2), room_location[1]))
        elif door_position == "top":
            self.grid[room_location[0], room_location[1] + int(room_size[1] / 2)] = -1
            self.obstacles.remove((room_location[0], room_location[1] + int(room_size[1] / 2)))
        elif door_position == "right":
            self.grid[room_location[0] + room_size[0] - 1, room_location[1] + int(room_size[1] / 2)] = -1

            if (
            room_location[0] + room_size[0], room_location[1] + np.random.randint(0, room_size[1])) in self.obstacles:
                self.obstacles.remove(
                    (room_location[0] + room_size[0], room_location[1] + np.random.randint(0, room_size[1])))

    ## Put methods here:

    def agent_on_map(self):
        """Prints out current location of the agent on the grid (used for debugging)"""
        self.grid[self.current_location[0], self.current_location[1]] = 0
        return self.grid

    def get_reward(self, new_location):
        """Returns the reward for an input position"""
        return self.grid[new_location[0], new_location[1]]

    def check_state(self):
        """Check if the agent is in a terminal state (gold or bomb), if so return 'TERMINAL'"""
        if self.current_location in self.terminal_states:
            return 'TERMINAL'


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # env = GridWorld()
    # print("Current position of the agent =", env.current_location)
    # print(env.agent_on_map())
    #
    # agent = ValueIterationAgent(env)
    # agent.value_iteration2()

    # plot the itern_num rooms_num
    # Create empty lists to store the data points
    rooms_nums = []
    iterations_nums = []
    #
    # env = GridWorld(num_rooms=40)
    # agent = ValueIterationAgent(env)
    # iterations_num = agent.value_iteration2()

    for rooms_num in range(1, 80, 10):
        # Perform the value iteration for each rooms_num
        env = GridWorld(num_rooms=rooms_num)
        agent = ValueIterationAgent(env)
        iterations_num = agent.value_iteration2()

        # Append the data points to the lists
        rooms_nums.append(rooms_num)
        iterations_nums.append(iterations_num)

    # Plot the data
    plt.plot(rooms_nums, iterations_nums)
    plt.xlabel('Number of Rooms')
    plt.ylabel('Number of Iterations')
    plt.title('Number of Iterations vs Number of Rooms')
    plt.show()
