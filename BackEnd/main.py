from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from GameFlow.startUp import mainInfo
import traceback

app = Flask(__name__)
CORS(app)

game = mainInfo()


@app.route('/api/start-game', methods=['POST'])
def start_game():
    """
    Start a game of Hide and Seek.

    Request body should contain the following:
    - rows: number of rows in the game world
    - cols: number of columns in the game world
    - gameMode: type of game, either 'human' or 'simulation'
    - playerRole: role of the human player, either 'hider' or 'seeker'

    Returns:
    - gameWorld: the game world as a 2D array
    - worldSize: the number of cells in the game world
    """
    try:
        data = request.json
        game.start(
            world_rows=data['rows'],
            world_cols=data['cols'],
            game_mode=0 if data['gameMode'] == 'human' else 1,
            human_player_mode=0 if data['playerRole'] == 'hider' else 1
        )
        return jsonify({
            'gameWorld': game.difficulty
        })
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500
@app.route('/api/play-round', methods=['POST'])
def play_round():
    """
    Play a round of Hide and Seek.

    Request body should contain the following:
    - playerRole: role of the human player, either 'hider' or 'seeker'
    - playerMove: the move of the human player in the game world

    Returns:
    - computerMove: the move of the computer (the opponent) in the game world
    - hiderScore: the score of the hider
    - seekerScore: the score of the seeker
    - gameWorld: the game world as a 2D array
    """
    try:
        data = request.json
        # Get the computer's move using linear programming
        row = data['playerMove'] // game.world_cols
        col = data['playerMove'] % game.world_cols
        game.formulate_game()
        result = game.solve_game_as_LP()
        computer_strategy = result.x[:-1]  # Extract probabilities
        computer_move = np.random.choice(len(computer_strategy), p=computer_strategy)
        computer_row = computer_move // game.world_cols
        computer_col = computer_move % game.world_cols
        if data['playerRole'] == 'hider':
            game.hider_plays(row, col)
            game.seeker_plays(computer_row, computer_col)
        else:
            game.hider_plays(computer_row, computer_col)
            game.seeker_plays(row, col)
            # computer_move = max(range(len(computer_strategy)),
            #                     key=lambda i: computer_strategy[i])
        # Return the computer's move and the current game state
        return jsonify({
            'computerMove': computer_move,
            'hiderScore': game.hider_score,
            'seekerScore': game.seeker_score,
            'probabilities': computer_strategy.tolist(),
        })
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500


@app.route('/api/simulate', methods=['POST'])
def simulate_game():
    """
    Simulate a game of Hide and Seek.

    Request body should contain the following:
    - rounds: the number of rounds to simulate (default is 100)

    Returns:
    - playerWins: the number of rounds won by the player
    - computerWins: the number of rounds won by the computer
    - playerScore: the total score of the player
    - computerScore: the total score of the computer
    - totalRounds: the total number of rounds simulated
    """
    try:
        data = request.json
        total_rounds = data.get('rounds', 100)  # Get total rounds from request
        player_wins = 0
        computer_wins = 0
        player_score = 0
        computer_score = 0
        rounds_results = []

        game.game_mode = 1  # Set to simulation mode

        game.resetGame()
        for _ in range(total_rounds):
            game.formulate_game()
            result = game.solve_game_as_LP()
            computer_strategy = result.x[:-1]
            player_move = np.random.choice(len(computer_strategy), p=computer_strategy)
            player_row = player_move // game.world_cols
            player_col = player_move % game.world_cols
            game.hider_plays(player_row, player_col)
            computer_move = np.random.choice(len(computer_strategy), p=computer_strategy)
            computer_row = computer_move // game.world_cols
            computer_col = computer_move % game.world_cols
            game.seeker_plays(computer_row, computer_col)

            if game.hider_score > game.seeker_score:
                player_wins += 1
            else:
                computer_wins += 1
            player_score += game.hider_score
            computer_score += game.seeker_score

            rounds_results.append({"winner" : "player" if game.hider_score > game.seeker_score else "computer", "hiderScore": game.hider_score, "seekerScore": game.seeker_score, "computerMove": computer_move, "playerMove": player_move})

        return jsonify({
            'playerWins': player_wins,
            'computerWins': computer_wins,
            'playerScore': player_score,
            'computerScore': computer_score,
            'totalRounds': total_rounds,
            'roundsResults': rounds_results,
        })
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)