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
    def hider_plays(self , i , j):
        self.hider_location = (i,j)
        self.payoff[(i + 1) * self.world_size + j][i * self.world_size + j] = 0.75 * self.payoff[
            (i + 1) * self.world_size + j][i * self.world_size + j]  # 4
        self.payoff[(i - 1) * self.world_size + j][i * self.world_size + j] = 0.75 * self.payoff[
            (i - 1) * self.world_size + j][i * self.world_size + j]  # 1
        self.payoff[i * self.world_size + j][i * self.world_size + j + 1] = 0.75 * self.payoff[i * self.world_size + j][
            i * self.world_size + j + 1]  # 2   #                        0.5(5)
        self.payoff[i * self.world_size + j][i * self.world_size + j - 1] = 0.75 * self.payoff[i * self.world_size + j][
            i * self.world_size + j - 1]  # 3    #             0.5(10)    0.75(1)        0.5 (9)
        self.payoff[(i + 2) * self.world_size + j][i * self.world_size + j] = 0.5 * self.payoff[
            (i + 2) * self.world_size + j][
            i * self.world_size + j]  # 8    #0.5 (7)      0.75(3)       x           0.75(2)    0.5 (6)
        self.payoff[(i - 2) * self.world_size + j][i * self.world_size + j] = 0.5 * self.payoff[
            (i - 2) * self.world_size + j][
            i * self.world_size + j]  # 5    #             0.5(12)    0.75(4)        0.5(11)
        self.payoff[i * self.world_size + j][i * self.world_size + j + 2] = 0.5 * self.payoff[i * self.world_size + j][
            i * self.world_size + j + 2]  # 6    #                        0.5 (8)
        self.payoff[i * self.world_size + j][i * self.world_size + j - 2] = 0.5 * self.payoff[i * self.world_size + j][
            i * self.world_size + j - 2]  # 7
        self.payoff[(i + 1) * self.world_size + j][i * self.world_size + j + 1] = 0.5 * self.payoff[
            (i + 1) * self.world_size + j][i * self.world_size + j + 1]  # 11
        self.payoff[(i + 1) * self.world_size + j][i * self.world_size + j - 1] = 0.5 * self.payoff[
            (i + 1) * self.world_size + j][i * self.world_size + j - 1]  # 12
        self.payoff[(i - 1) * self.world_size + j][i * self.world_size + j + 1] = 0.5 * self.payoff[
            (i - 1) * self.world_size + j][i * self.world_size + j + 1]  # 9
        self.payoff[(i - 1) * self.world_size + j][i * self.world_size + j - 1] = 0.5 * self.payoff[
            (i - 1) * self.world_size + j][i * self.world_size + j - 1]  # 10
        self.formulate_game()

    def seeker_plays(self , i , j):
        if abs(i - self.hider_location[0]) + abs(j - self.hider_location[1]) == 0:
            self.seeker_score = self.seeker_score + abs(self.payoff[i * self.world_cols + j])
        else:  # elif (abs(i-self.hider_location[0])+abs(j-self.hider_location[1]) == 1):
            self.hider_score = self.hider_score + abs(self.payoff[i * self.world_cols + j])
        # elif (abs(i-self.hider_location[0])+abs(j-self.hider_location[1]) == 2):
        #     self.hider_score = self.hider_score + abs(self.payoff[i*self.world_cols+j])

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
        result = linprog(c=[0]*self.world_size+ [-1], A_ub=A, b_ub=b, A_eq=[[1]*self.world_size+[0]], b_eq=[1], bounds=bounds, method='highs')
        # print gain value
        print("Gain value: ", result.x[-1])
        return result
        
