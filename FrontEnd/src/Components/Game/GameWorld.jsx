import './GameWorld.css';

export default function GameWorld({
    gameWorld,
    playerMove,
    computerMove,
    placeTypeLabels,
    placeTypeColors,
    onPlaceClick,
    playerRole,
    showResult
}) {
    return (
        <div className="gameworld-container">
            <h2 className="gameworld-title">Game World</h2>
            <div className="gameworld-places">
                {gameWorld.map((type, index) => {
                    // Only show color and label after round is played
                    const colorClass = showResult && placeTypeColors ? placeTypeColors[type] : 'gameworld-label-neutral';
                    const isSelected = playerMove === index;
                    const isComputer = showResult && computerMove === index;
                    return (
                        <button
                            key={index}
                            className={`gameworld-place ${colorClass} ${isSelected ? 'selected' : ''} ${isComputer ? 'computer' : ''}`}
                            onClick={() => onPlaceClick(index)}
                            disabled={showResult}
                        >
                            <div>
                                <div>{index + 1}</div>
                                <div>
                                    {showResult ? placeTypeLabels[type] : ''}
                                </div>
                            </div>
                        </button>
                    );
                })}
            </div>
            {showResult && (
                <div className="gameworld-labels">
                    <span className="gameworld-label-neutral"></span> Neutral
                    <span className="gameworld-label-easy"></span> Easy for Seeker
                    <span className="gameworld-label-hard"></span> Hard for Seeker
                </div>
            )}
        </div>
    );
}