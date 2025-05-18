import './GameWorld.css';

export default function GameWorld({
    gameWorld,
    playerMove,
    computerMove,
    placeTypeLabels,
    placeTypeColors,
    onPlaceClick,
    playerRole,
    showResult,
    worldMode
}) {
    const renderCell = (type, index) => {
        const colorClass = placeTypeColors ? placeTypeColors[type] : 'gameworld-label-neutral';
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
                </div>
            </button>
        );
    };

    const renderGrid = () => {
        return gameWorld.map((row, rowIndex) => (
            <div key={rowIndex} className="gameworld-row">
                {row.map((cell, colIndex) => {
                    const index = rowIndex * row.length + colIndex;
                    return renderCell(cell, index);
                })}
            </div>
        ));
    };

    const renderLinear = () => {
        return gameWorld.map((cell, index) => renderCell(cell, index));
    };

    return (
        <div className="gameworld-container">
            <h2 className="gameworld-title">Game World</h2>
            <div className={`gameworld-places ${worldMode === 'grid' ? 'grid-layout' : ''}`}>
                {Array.isArray(gameWorld[0]) ? renderGrid() : renderLinear()}
            </div>
            <div className="gameworld-labels">
                <span className="gameworld-label-neutral"></span> Neutral
                <span className="gameworld-label-easy"></span> Easy for Seeker
                <span className="gameworld-label-hard"></span> Hard for Seeker
            </div>
        </div>
    );
}