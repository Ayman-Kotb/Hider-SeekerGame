import './ScoreBoard.css';
export default function ScoreBoard({ playerRole, playerScore, computerScore }) {
    return (
        <div>
            <div>
                <h2>Your Role: {playerRole === 'hider' ? 'Hider' : 'Seeker'}</h2>
                <p>Your Score: {playerScore}</p>
            </div>
            <div>
                <h2>Computer's Role: {playerRole === 'hider' ? 'Seeker' : 'Hider'}</h2>
                <p>Computer's Score: {computerScore}</p>
            </div>
        </div>
    );
}