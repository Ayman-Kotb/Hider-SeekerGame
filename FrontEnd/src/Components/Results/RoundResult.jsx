import './RoundResult.css';

export default function RoundResult({ roundResult, onNextRound }) {
    return (
        <div className={`roundresult-container ${roundResult.winner === 'player' ? 'roundresult-win' : 'roundresult-lose'}`}>
            <h3 className="roundresult-title">Round Result</h3>
            <p>
                {roundResult.winner === 'player'
                    ? `You won! You earned ${roundResult.score} points.`
                    : `Computer won! Computer earned ${roundResult.score} points.`}
            </p>
            <button
                className="roundresult-btn"
                onClick={onNextRound}
            >
                Next Round
            </button>
        </div>
    );
}