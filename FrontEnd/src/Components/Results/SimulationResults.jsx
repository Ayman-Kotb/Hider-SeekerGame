import './SimulationResults.css';

export default function SimulationResults({ simulationResults }) {
    return (
        <div className="simulationresults-container">
            <h3 className="simulationresults-title">Simulation Results (100 Rounds)</h3>
            <div className="simulationresults-grid">
                <div>
                    <p>Player Wins: {simulationResults.playerWins}</p>
                    <p>Player Score: {simulationResults.playerScore}</p>
                </div>
                <div>
                    <p>Computer Wins: {simulationResults.computerWins}</p>
                    <p>Computer Score: {simulationResults.computerScore}</p>
                </div>
            </div>
        </div>
    );
}