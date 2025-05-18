from flask import Flask, request, jsonify
from flask_cors import CORS
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
        if data['playerRole'] == 'hider':
            # Get the row and column of the human player's move
            row = data['playerMove'] // game.world_cols
            col = data['playerMove'] % game.world_cols
            # Update the game state
            game.hider_plays(row, col)
        else:
            # Get the row and column of the human player's move
            row = data['playerMove'] // game.world_cols
            col = data['playerMove'] % game.world_cols
            # Update the game state
            game.seeker_plays(row, col)

        # Get the computer's move using linear programming
        game.formulate_game()
        result = game.solve_game_as_LP()
        computer_strategy = result.x[:-1]  # Extract probabilities
        # Find the move with the highest probability
        computer_move = max(range(len(computer_strategy)),
                            key=lambda i: computer_strategy[i])


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

        game.game_mode = 1  # Set to simulation mode

        for _ in range(total_rounds):
            game.formulate_game()
            result = game.solve_game_as_LP()
            computer_strategy = result.x[:-1]
            computer_move = max(range(len(computer_strategy)), key=lambda i: computer_strategy[i])
            game.seeker_plays(computer_move // game.world_cols, computer_move % game.world_cols)

            if game.hider_score > game.seeker_score:
                player_wins += 1
                player_score += game.hider_score
            else:
                computer_wins += 1
                computer_score += game.seeker_score

        return jsonify({
            'playerWins': player_wins,
            'computerWins': computer_wins,
            'playerScore': player_score,
            'computerScore': computer_score,
            'totalRounds': total_rounds
        })
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)