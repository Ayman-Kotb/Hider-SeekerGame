from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
from GameFlow.startUp import GameService

app = Flask(__name__)
CORS(app)

# Initialize game service
game_service = GameService()


@app.route('/api/start-game', methods=['POST'])
def start_game():
    try:
        data = request.json

        # Validate input
        if not all(key in data for key in ['rows', 'cols', 'gameMode', 'playerRole']):
            return jsonify({'error': 'Missing required parameters'}), 400

        # Call service method
        result = game_service.start_new_game(
            rows=data['rows'],
            cols=data['cols'],
            game_mode_str=data['gameMode'],
            player_role_str=data['playerRole']
        )

        if result['success']:
            return jsonify({
                'gameWorld': result['gameWorld'],
                'payoff': result['payoff'],
                'probabilities': result['probabilities']
            })
        else:
            return jsonify({'error': result['error']}), 500

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/api/play-round', methods=['POST'])
def play_round():
    try:
        data = request.json

        # Validate input
        if not all(key in data for key in ['playerRole', 'playerMove']):
            return jsonify({'error': 'Missing required parameters'}), 400

        # Call service method
        result = game_service.play_game_round(
            player_role_str=data['playerRole'],
            player_move=data['playerMove']
        )

        if result['success']:
            return jsonify({
                'computerMove': result['computerMove'],
                'hiderScore': result['hiderScore'],
                'seekerScore': result['seekerScore'],
                'probabilities': result['probabilities']
            })
        else:
            return jsonify({'error': result['error']}), 500

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/api/simulate', methods=['POST'])
def simulate_game():
    try:
        data = request.json
        rounds = data.get('rounds', 100)

        # Validate input
        if not isinstance(rounds, int) or rounds <= 0:
            return jsonify({'error': 'Rounds must be a positive integer'}), 400

        # Call service method
        result = game_service.simulate_game_rounds(rounds)

        if result['success']:
            return jsonify({
                'probabilitiesOfHider': result['probabilitiesOfHider'],
                'probabilitiesOfSeeker': result['probabilitiesOfSeeker'],
                'playerWins': result['playerWins'],
                'computerWins': result['computerWins'],
                'playerScore': result['playerScore'],
                'computerScore': result['computerScore'],
                'totalRounds': result['totalRounds'],
                'roundsResults': result['roundsResults']
            })
        else:
            return jsonify({'error': result['error']}), 500

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Hide and Seek API is running'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)