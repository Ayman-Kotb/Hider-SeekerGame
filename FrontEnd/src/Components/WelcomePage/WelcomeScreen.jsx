import './WelcomeScreen.css';

export default function WelcomeScreen({ worldSize, onSizeChange, onStartGame }) {
    return (
        <div className="welcome-container">
            <div className="welcome-box">
                <h1 className="welcome-title">Hide & Seek Game</h1>
                <div className="welcome-content">
                    <p className="welcome-text">
                        Welcome to the Hide & Seek game!
                    </p>
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