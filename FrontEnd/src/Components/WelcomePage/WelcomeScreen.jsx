import './WelcomeScreen.css';

export default function WelcomeScreen({ worldSize, onSizeChange, onStartGame, rows, handleRowChange, cols, handleColsChange, worldMode, setWorldMode }) {
    return (
        <div className="welcome-container">
            <div className="welcome-box">
                <h1 className="welcome-title">Hide & Seek Game</h1>
                <div className="welcome-content">
                    <p className="welcome-text">
                        Welcome to the Hide & Seek game!
                    </p>
                    <div className="welcome-input-group">
                        <label className="welcome-label">World Mode:</label>
                        <select 
                            value={worldMode} 
                            onChange={(e) => {
                                setWorldMode(e.target.value);
                            }}
                            className="welcome-input"
                        >
                            <option value="linear">Linear</option>
                            <option value="grid">Grid</option>
                        </select>
                    </div>

                    {worldMode === 'linear' ? (
                        <div className="welcome-input-group">
                            <label className="welcome-label">World Size:</label>
                            <input
                                type="number"
                                min="1"
                                value={worldSize}
                                onChange={onSizeChange}
                                className="welcome-input"
                            />
                        </div>
                    ) : (
                        <>
                            <div className="welcome-input-group">
                                <label className="welcome-label">Rows:</label>
                                <input
                                    type="number"
                                    min="1"
                                    value={rows}
                                    onChange={(e) => {
                                            handleRowChange(Number(e.target.value));
                                    }}
                                    className="welcome-input"
                                />
                            </div>
                            <div className="welcome-input-group">
                                <label className="welcome-label">Columns:</label>
                                <input
                                    type="number"
                                    min="1"
                                    value={cols}
                                    onChange={(e) => {
                                        handleColsChange(Number(e.target.value)); 
                                    }}
                                    className="welcome-input"
                                />
                            </div>
                        </>
                    )}
                </div>
                <div className="welcome-buttons">
                    <button
                        onClick={() => onStartGame('hider')}
                        className="welcome-btn hider"
                    >
                        Play as Hider
                    </button>
                    <button
                        onClick={() => onStartGame('seeker')}
                        className="welcome-btn seeker"
                    >
                        Play as Seeker
                    </button>
                </div>
            </div>
        </div>
    );
}