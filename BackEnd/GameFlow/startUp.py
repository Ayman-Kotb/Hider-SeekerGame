import numpy as np
from scipy.optimize import linprog
import random

class mainInfo: # we get this info from the first page from user
    world_rows = 0
    world_cols = 0
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
        for i in range (size):
            x = random.randint(0, 2147483640)%3
            level[i] = x
            if level[i] == 0: #easy
                world[i] = [2] *size
                world[i][i] = -1
                if (i+1<size):
                    world[i][i+1] = 2 *0.5
                if (i-1>-1):
                    world [i][i-1] = 2 *0.5
                if (i+2<size):
                    world[i][i+2] = 2 *0.75
                if (i-2>-1):
                    world [i][i-2] = 2 *0.75
            elif level[i] == 1: #med
                world[i] = [1] *size
                world[i][i] = -1
                if (i+1<size):
                    world[i][i+1] = 1 *0.5
                if (i-1>-1):
                    world [i][i-1] = 1 *0.5
                if (i+2<size):
                    world[i][i+2] = 1 *0.75
                if (i-2>-1):
                    world [i][i-2] = 1 *0.75
            elif level[i] == 2: #hard
                world[i] = [1] * size
                world[i][i] = -3
                if (i+1<size):
                    world[i][i+1] = 1 *0.5
                if (i-1>-1):
                    world [i][i-1] = 1 *0.5
                if (i+2<size):
                    world[i][i+2] = 1 *0.75
                if (i-2>-1):
                    world [i][i-2] = 1 *0.75
        print(world)
        diffecultyArr = [[0 for _ in range(self.world_cols)] for _ in range(self.world_rows)]
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
        #def safe_update_payoff(row1, col1, row2, col2, factor):
        #     # Make sure coordinates are within bounds using modulo
        #     row1 = row1 % self.world_rows
        #     col1 = col1 % self.world_cols
        #     row2 = row2 % self.world_rows
        #     col2 = col2 % self.world_cols

        #     # Calculate positions in flattened grid
        #     pos1 = row1 * self.world_cols + col1
        #     pos2 = row2 * self.world_cols + col2

        #     # Check if indices are within payoff matrix bounds
        #     if 0 <= pos1 < len(self.payoff) and 0 <= pos2 < len(self.payoff[0]):
        #         self.payoff[pos1][pos2] *= factor

        # # Update payoffs for direct neighbors (factor 0.5)
        # safe_update_payoff(i + 1, j, i, j, 0.5)  # Down
        # safe_update_payoff(i - 1, j, i, j, 0.5)  # Up
        # safe_update_payoff(i, j, i, j + 1, 0.5)  # Right
        # safe_update_payoff(i, j, i, j - 1, 0.5)  # Left

        # # Update payoffs for positions two steps away (factor 0.75)
        # safe_update_payoff(i + 2, j, i, j, 0.75)  # Down 2
        # safe_update_payoff(i - 2, j, i, j, 0.75)  # Up 2
        # safe_update_payoff(i, j, i, j + 2, 0.75)  # Right 2
        # safe_update_payoff(i, j, i, j - 2, 0.75)  # Left 2

        # # Update payoffs for diagonal neighbors (factor 0.75)
        # safe_update_payoff(i + 1, j, i, j + 1, 0.75)  # Down-Right
        # safe_update_payoff(i + 1, j, i, j - 1, 0.75)  # Down-Left
        # safe_update_payoff(i - 1, j, i, j + 1, 0.75)  # Up-Right
        # safe_update_payoff(i - 1, j, i, j - 1, 0.75)  # Up-Left

        # # Update game state
        #self.formulate_game()

    def seeker_plays(self , i , j):
        print(self.difficulty)
        print(self.payoff)
        print ("location of hider : ")
        print(self.hider_location[0] * self.world_rows + self.hider_location[1])
        print ("location of seeker : ")
        print(i * self.world_rows + j)
        if abs(i - self.hider_location[0]) + abs(j - self.hider_location[1]) == 0:
            
            self.seeker_score =   abs(self.payoff[self.hider_location[0] * self.world_rows + self.hider_location[1]][i*self.world_rows + j])*4
            self.hider_score =  -abs(self.payoff[self.hider_location[0] * self.world_rows + self.hider_location[1]][i*self.world_rows + j])*4
        else:  # elif (abs(i-self.hider_location[0])+abs(j-self.hider_location[1]) == 1):
            self.hider_score =   abs(self.payoff[self.hider_location[0] * self.world_rows + self.hider_location[1]][i*self.world_rows + j])*4
            self.seeker_score =  -abs(self.payoff[self.hider_location[0] * self.world_rows + self.hider_location[1]][i*self.world_rows + j])*4
        # # elif (abs(i-self.hider_location[0])+abs(j-self.hider_location[1]) == 2):
        #     self.hider_score = self.hider_score + abs(self.payoff[i*self.world_cols+j])

    def resetGame (self):
        self.hider_score = 0
        self.seeker_score = 0
        self.hider_location = (-1,-1)
    def formulate_game(self):
        if self.human_player_mode == 0:
            self.coeff = [row[:] for row in self.payoff]  #hider -> max of min of coeff. 
        else:
            self.coeff = [list(col) for col in zip(*self.payoff)]  #seeker -> min of max of coeff

    def solve_game_as_LP(self):
        bounds = [(0, 1)] * self.world_size + [(None, None)]
        A=[]
        b=[]
        if self.human_player_mode == 0:  # hider -> max of min of coeff.
            for j in range(self.world_size):
                row = [-self.coeff[i][j] for i in range(self.world_size)] + [1]  # -payoff + v ≤ 0
                A.append(row)
                b.append(0)
        else:                              # seeker -> min of max of coeff
            for i in range(self.world_size):
                row = [self.coeff[i][j] for j in range(self.world_size)] + [-1]  # payoff - v ≤ 0
                A.append(row)
                b.append(0)
        # print ("i am A matrix"+A)
        result = linprog(c=[0]*self.world_size+ [-1], A_ub=A, b_ub=b, A_eq=[[1]*self.world_size+[0]], b_eq=[1], bounds=bounds, method='highs')
        # print gain value
        # print("Gain value: ", result.x[-1])
        return result
