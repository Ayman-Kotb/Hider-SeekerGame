import numpy as np
from scipy.optimize import linprog
import random


class HideAndSeekGame:
    """Main game class for Hide and Seek game logic"""

    def __init__(self):
        self.world_rows = 0
        self.world_cols = 0
        self.world_size = 0
        self.hider_score = 0
        self.seeker_score = 0
        self.coeff = []
        self.world = []
        self.payoff = []
        self.difficulty = []
        self.game_mode = 0  # 0 human vs. computer, 1 computer simulation
        self.human_player_mode = 0  # 0 player is hider, 1 player is seeker
        self.hider_location = (-1, -1)

    def initialize_game(self, world_rows, world_cols, game_mode, human_player_mode):
        """Initialize a new game with the given parameters"""
        self.world_rows = world_rows
        self.world_cols = world_cols
        self.world_size = world_cols * world_rows
        self.game_mode = game_mode
        self.human_player_mode = human_player_mode
        self.hider_location = (-1, -1)

        # Initialize matrices
        self.coeff = [[0 for _ in range(self.world_size)] for _ in range(self.world_size)]
        self.world = [[0 for _ in range(world_cols)] for _ in range(world_rows)]

        # Generate random world and difficulty
        self.payoff, self.difficulty = self._generate_random_world()

        return {
            'gameWorld': self.difficulty,
            'payoff': self.payoff,
            'worldSize': self.world_size
        }

    def _generate_random_world(self):
        """Generate random world with different difficulty levels"""
        size = self.world_size
        rows = self.world_rows
        cols = self.world_cols

        level = [random.randint(0, 2) for _ in range(size)]
        world = [[0 for _ in range(size)] for _ in range(size)]

        for i in range(size):
            current_row = i // cols
            current_col = i % cols

            if level[i] == 0:  # easy
                world[i] = [2] * size
                world[i][i] = -1
                self._set_neighbor_payoffs(world, i, current_row, current_col, rows, cols, size, 2)

            elif level[i] == 1:  # medium
                world[i] = [1] * size
                world[i][i] = -1
                self._set_neighbor_payoffs(world, i, current_row, current_col, rows, cols, size, 1)

            elif level[i] == 2:  # hard
                world[i] = [1] * size
                world[i][i] = -3
                self._set_neighbor_payoffs(world, i, current_row, current_col, rows, cols, size, 1)

        # Create a difficulty array for 2D representation
        difficulty_arr = [[0 for _ in range(self.world_cols)] for _ in range(self.world_rows)]
        for i in range(self.world_rows):
            for j in range(self.world_cols):
                difficulty_arr[i][j] = level[i * self.world_cols + j]

        return world, difficulty_arr

    def _set_neighbor_payoffs(self, world, i, current_row, current_col, rows, cols, size, base_value):
        """Set payoffs for neighboring cells"""
        # Horizontal neighbors (left/right)
        if ((i + 1) // cols) == current_row and i + 1 < size:
            world[i][i + 1] = base_value * 0.5
        if ((i - 1) // cols) == current_row and i - 1 >= 0:
            world[i][i - 1] = base_value * 0.5
        if ((i + 2) // cols) == current_row and i + 2 < size:
            world[i][i + 2] = base_value * 0.75
        if ((i - 2) // cols) == current_row and i - 2 >= 0:
            world[i][i - 2] = base_value * 0.75

        # Vertical neighbors (up/down)
        if current_row + 1 < rows:
            world[i][i + cols] = base_value * 0.5
        if current_row - 1 >= 0:
            world[i][i - cols] = base_value * 0.5
        if current_row + 2 < rows:
            world[i][i + 2 * cols] = base_value * 0.75
        if current_row - 2 >= 0:
            world[i][i - 2 * cols] = base_value * 0.75

        # Diagonal neighbors
        if current_row + 1 < rows and current_col + 1 < cols:
            world[i][i + cols + 1] = base_value * 0.75
        if current_row - 1 >= 0 and current_col + 1 < cols:
            world[i][i - cols + 1] = base_value * 0.75
        if current_row + 1 < rows and current_col - 1 >= 0:
            world[i][i + cols - 1] = base_value * 0.75
        if current_row - 1 >= 0 and current_col - 1 >= 0:
            world[i][i - cols - 1] = base_value * 0.75

    def make_hider_move(self, row, col):
        """Process hider's move"""
        self.hider_location = (row, col)

    def make_seeker_move(self, row, col):
        """Process seeker's move and calculate scores"""
        hider_pos = self.hider_location[0] * self.world_cols + self.hider_location[1]
        seeker_pos = row * self.world_cols + col

        # Calculate Manhattan distance
        distance = abs(row - self.hider_location[0]) + abs(col - self.hider_location[1])

        if distance == 0:  # Seeker found hider
            payoff_value = abs(self.payoff[hider_pos][seeker_pos])
            self.seeker_score = payoff_value * 4
            self.hider_score = -payoff_value * 4
        else:  # Seeker didn't find hider
            payoff_value = abs(self.payoff[hider_pos][seeker_pos])
            self.hider_score = payoff_value * 4
            self.seeker_score = -payoff_value * 4

        return {
            'hiderScore': self.hider_score,
            'seekerScore': self.seeker_score
        }

    def reset_game(self):
        """Reset game scores and hider location"""
        self.hider_score = 0
        self.seeker_score = 0
        self.hider_location = (-1, -1)

    def formulate_game_matrix(self):
        """Formulate the game matrix based on player mode"""
        if self.human_player_mode == 0:  # Human is hider
            self.coeff = [row[:] for row in self.payoff]
        else:  # Human is seeker
            self.coeff = [list(col) for col in zip(*self.payoff)]

    def solve_optimal_strategy(self):
        """Solve for optimal mixed strategy using Linear Programming"""
        bounds = [(0, 1)] * self.world_size + [(None, None)]
        A = []
        b = []
        c = []

        if self.human_player_mode == 0:  # Human is hider -> maximize minimum
            c = [0] * self.world_size + [-1]  # maximize v
            for j in range(self.world_size):
                row = [-self.coeff[i][j] for i in range(self.world_size)] + [1]
                A.append(row)
                b.append(0)
        else:  # Human is seeker -> minimize maximum
            c = [0] * self.world_size + [1]  # minimize v
            for i in range(self.world_size):
                row = [self.coeff[i][j] for j in range(self.world_size)] + [-1]
                A.append(row)
                b.append(0)

        result = linprog(
            c=c,
            A_ub=A,
            b_ub=b,
            A_eq=[[1] * self.world_size + [0]],
            b_eq=[1],
            bounds=bounds,
            method='highs'
        )

        return result


class GameService:
    """Service class to handle game operations"""

    def __init__(self):
        self.game = HideAndSeekGame()

    def start_new_game(self, rows, cols, game_mode_str, player_role_str):
        """Start a new game and return initial game state"""
        try:
            game_mode = 0 if game_mode_str == 'human' else 1
            human_player_mode = 0 if player_role_str == 'hider' else 1

            game_data = self.game.initialize_game(rows, cols, game_mode, human_player_mode)

            # Get computer strategy
            self.game.formulate_game_matrix()
            result = self.game.solve_optimal_strategy()
            computer_strategy = result.x[:-1]

            return {
                'success': True,
                'gameWorld': game_data['gameWorld'],
                'payoff': game_data['payoff'],
                'probabilities': computer_strategy.tolist()
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def play_game_round(self, player_role_str, player_move):
        """Play a single round of the game"""
        try:
            # Convert player move to coordinates
            row = player_move // self.game.world_cols
            col = player_move % self.game.world_cols

            # Get computer strategy
            self.game.formulate_game_matrix()
            result = self.game.solve_optimal_strategy()
            computer_strategy = result.x[:-1]
            computer_move = np.random.choice(len(computer_strategy), p=computer_strategy)
            computer_row = computer_move // self.game.world_cols
            computer_col = computer_move % self.game.world_cols

            # Execute moves based on a player role
            if player_role_str == 'hider':
                self.game.make_hider_move(row, col)
                scores = self.game.make_seeker_move(computer_row, computer_col)
            else:
                self.game.make_hider_move(computer_row, computer_col)
                scores = self.game.make_seeker_move(row, col)

            return {
                'success': True,
                'computerMove': computer_move,
                'hiderScore': scores['hiderScore'],
                'seekerScore': scores['seekerScore'],
                'probabilities': computer_strategy.tolist()
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def simulate_game_rounds(self, rounds):
        """Simulate multiple rounds of computer vs computer play"""
        try:
            # Reset game for simulation
            self.game.game_mode = 1
            self.game.reset_game()

            # Get strategies for both players
            self.game.human_player_mode = 0  # Hider strategy
            self.game.formulate_game_matrix()
            hider_result = self.game.solve_optimal_strategy()

            self.game.human_player_mode = 1  # Seeker strategy
            self.game.formulate_game_matrix()
            seeker_result = self.game.solve_optimal_strategy()

            # Simulation variables
            player_wins = 0
            computer_wins = 0
            player_score = 0
            computer_score = 0
            rounds_results = []

            for _ in range(rounds):
                # Get moves for both players
                hider_strategy = hider_result.x[:-1]
                player_move = np.random.choice(len(hider_strategy), p=hider_strategy)
                player_row = player_move // self.game.world_cols
                player_col = player_move % self.game.world_cols

                seeker_strategy = seeker_result.x[:-1]
                computer_move = np.random.choice(len(seeker_strategy), p=seeker_strategy)
                computer_row = computer_move // self.game.world_cols
                computer_col = computer_move % self.game.world_cols

                # Execute moves
                self.game.make_hider_move(player_row, player_col)
                scores = self.game.make_seeker_move(computer_row, computer_col)

                # Track results
                if scores['hiderScore'] > scores['seekerScore']:
                    player_wins += 1
                else:
                    computer_wins += 1

                player_score += scores['hiderScore']
                computer_score += scores['seekerScore']

                rounds_results.append({
                    "winner": "player" if scores['hiderScore'] > scores['seekerScore'] else "computer",
                    "hiderScore": scores['hiderScore'],
                    "seekerScore": scores['seekerScore'],
                    "computerMove": computer_move,
                    "playerMove": player_move
                })

            return {
                'success': True,
                'probabilitiesOfHider': hider_result.x[:-1].tolist(),
                'probabilitiesOfSeeker': seeker_result.x[:-1].tolist(),
                'playerWins': player_wins,
                'computerWins': computer_wins,
                'playerScore': player_score,
                'computerScore': computer_score,
                'totalRounds': rounds,
                'roundsResults': rounds_results
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}