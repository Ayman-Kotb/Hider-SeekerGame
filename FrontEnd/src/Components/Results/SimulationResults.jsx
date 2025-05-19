import './SimulationResults.css';

export default function SimulationResults({ simulationResults }) {
    return (
        <div className="simulationresults-container">
            <h3 className="simulationresults-title">Simulation Results ({simulationResults.totalRounds} Rounds)</h3>
            <div className="simulationresults-grid">
                <div className="simulationresults-card player">
                    <p>Player Wins: {simulationResults.playerWins}</p>
                    <p>Player Score: {simulationResults.playerScore}</p>
                </div>
                <div className="simulationresults-card computer">
                    <p>Computer Wins: {simulationResults.computerWins}</p>
                    <p>Computer Score: {simulationResults.computerScore}</p>
                </div>
            </div>
            <div className="simulationresults-rounds">
                <h4>Rounds Details</h4>
                <table className="simulationresults-table">
                    <thead>
                        <tr>
                            <th>Round</th>
                            <th>Winner</th>
                            <th>Hider Move</th>
                            <th>Seeker Move</th>
                            <th>Hider Score</th>
                            <th>Seeker Score</th>
                        </tr>
                    </thead>
                    <tbody>
                        {simulationResults.roundsResults && simulationResults.roundsResults.map((r, i) => (
                            <tr key={i} className={r.winner === "player" ? "round-player" : "round-computer"}>
                                <td>{i + 1}</td>
                                <td>{r.winner}</td>
                                <td>{r.playerMove}</td>
                                <td>{r.computerMove}</td>
                                <td>{r.hiderScore}</td>
                                <td>{r.seekerScore}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}