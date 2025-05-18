import numpy as np
from scipy.optimize import linprog
import random

class mainInfo: # we get this info from the first page from user
    world_rows = 10
    world_cols = 10
    world_size = 0
    hider_score = 0
    seeker_score = 0
    coeff =[]
    world = [] # it includes elements as the number of places that hider can hide in
    payoff = [] # generate random values according to levels (med −1 1 1 1) (easy 2 −1 2 2) (hard 1 1 −3 1)
    # it includes rows as the number of places that hider can hide in
    difficulty = [] # it includes elements as the number of places that hider can hide in
    game_mode = 0  # 0 human computers, 1 computer (simulation)
    human_player_mode = 0 # 0 player hider , 1 player seeker

    def __init__(self):
        self.hider_location = None

    def start(self, world_rows,world_cols,game_mode,human_player_mode):
        self.world_rows = world_rows
        self.hider_location = (-1,-1)
        self.world_cols = world_cols
        self.world_size = world_cols * world_rows
        self.game_mode = game_mode
        self.coeff = [[0 for _ in range(self.world_size)] for _ in range(self.world_size)]
        self.world = [[0 for _ in range(world_cols)] for _ in range(world_rows)]
        self.human_player_mode = human_player_mode
        self.payoff, self.difficulty = self.random_world(self.world_size)

    def random_world(self , size):
        level = [0] * size
        world = [[0 for _ in range(size)] for _ in range(size)]
        for i in range(size):
            x = random.randint(0, 2147483640)%3
            level[i] = x
        for i in range (size):
            if level[i] == 0: #easy
                world[i] = [2] *size
                world[i][i] = -1
            elif level[i] == 1: #med
                world[i] = [1] *size
                world[i][i] = -1
            elif level[i] == 2: #hard
                world[i] = [1] * size
                world[i][i] = -3

        diffecultyArr = [[0]*self.world_cols] * self.world_rows
        for i in range(self.world_rows):
            for j in range(self.world_cols):
                diffecultyArr[i][j] = level[i * self.world_cols + j]
               
        return world, diffecultyArr

    def hider_plays(self, i, j):
        """
        Updates payoff matrix when the hider plays at position (i,j)
        Uses modulo arithmetic to handle edge cases
        """
        # Store hider's location
        self.hider_location = (i, j)

        # Current position index in flattened grid
        current_pos = i * self.world_cols + j

        # Create a safe update function that checks bounds
        def safe_update_payoff(row1, col1, row2, col2, factor):
            # Make sure coordinates are within bounds using modulo
            row1 = row1 % self.world_rows
            col1 = col1 % self.world_cols
            row2 = row2 % self.world_rows
            col2 = col2 % self.world_cols

            # Calculate positions in flattened grid
            pos1 = row1 * self.world_cols + col1
            pos2 = row2 * self.world_cols + col2

            # Check if indices are within payoff matrix bounds
            if 0 <= pos1 < len(self.payoff) and 0 <= pos2 < len(self.payoff[0]):
                self.payoff[pos1][pos2] *= factor

        # Update payoffs for direct neighbors (factor 0.5)
        safe_update_payoff(i + 1, j, i, j, 0.5)  # Down
        safe_update_payoff(i - 1, j, i, j, 0.5)  # Up
        safe_update_payoff(i, j, i, j + 1, 0.5)  # Right
        safe_update_payoff(i, j, i, j - 1, 0.5)  # Left

        # Update payoffs for positions two steps away (factor 0.75)
        safe_update_payoff(i + 2, j, i, j, 0.75)  # Down 2
        safe_update_payoff(i - 2, j, i, j, 0.75)  # Up 2
        safe_update_payoff(i, j, i, j + 2, 0.75)  # Right 2
        safe_update_payoff(i, j, i, j - 2, 0.75)  # Left 2

        # Update payoffs for diagonal neighbors (factor 0.75)
        safe_update_payoff(i + 1, j, i, j + 1, 0.75)  # Down-Right
        safe_update_payoff(i + 1, j, i, j - 1, 0.75)  # Down-Left
        safe_update_payoff(i - 1, j, i, j + 1, 0.75)  # Up-Right
        safe_update_payoff(i - 1, j, i, j - 1, 0.75)  # Up-Left

        # Update game state
        self.formulate_game()

    def seeker_plays(self , i , j):
        if abs(i - self.hider_location[0]) + abs(j - self.hider_location[1]) == 0:
            self.seeker_score = self.seeker_score + abs(self.payoff[i * self.world_cols + j])
        else:  # elif (abs(i-self.hider_location[0])+abs(j-self.hider_location[1]) == 1):
            self.hider_score = self.hider_score + abs(self.payoff[i * self.world_cols + j])
        # elif (abs(i-self.hider_location[0])+abs(j-self.hider_location[1]) == 2):
        #     self.hider_score = self.hider_score + abs(self.payoff[i*self.world_cols+j])

    def formulate_game(self):
        """
        Ensure the payoff matrix is correctly formatted before solving
        """
        # Check if the payoff matrix is properly initialized
        rows = len(self.payoff)
        if rows == 0:
            raise ValueError("Payoff matrix is empty")

        # Ensure all rows have the same number of columns
        cols = len(self.payoff[0])
        for row in self.payoff:
            if len(row) != cols:
                # Pad with zeros if necessary
                row.extend([0] * (cols - len(row)))

        # Ensure the matrix is rectangular (needed for linprog)
        self.payoff = np.array(self.payoff, dtype=float)

    def solve_game_as_LP(self):
        """
        Solve the game using linear programming with proper dimension handling
        """
        try:
            # Get dimensions
            m, n = self.payoff.shape

            # For zero-sum games, we use the standard LP formulation
            c = np.zeros(n + 1)
            c[-1] = -1  # Objective is to maximize the game value

            # Constraints: each row of payoff matrix
            A_ub = np.hstack([self.payoff, -np.ones((m, 1))])
            b_ub = np.zeros(m)

            # Simplex constraints: probabilities sum to 1
            A_eq = np.ones((1, n + 1))
            A_eq[0, -1] = 0
            b_eq = np.ones(1)

            # Bounds: probabilities are non-negative, v is unconstrained
            bounds = [(0, None) for _ in range(n)] + [(None, None)]

            # Solve using scipy's linprog
            result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='simplex')

            return result

        except Exception as e:
            print(f"Linear programming error: {str(e)}")
            # Return a fallback strategy (uniform distribution)
            fallback = np.ones(n) / n

            class FallbackResult:
                def __init__(self, strategy):
                    self.x = np.append(strategy, 0)  # Add dummy value for consistency
                    self.success = False
                    self.message = "Used fallback strategy due to LP error"

            return FallbackResult(fallback)
        
