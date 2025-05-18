import { useState } from 'react';
import WelcomeScreen from './WelcomePage/WelcomeScreen';
import ScoreBoard from './ScoreBoard/ScoreBoard';
import GameWorld from './Game/GameWorld';
import RoundResult from './Results/RoundResult';
import SimulationResults from './Results/SimulationResults';
import './HideAndSeekGame.css';

export default function HideAndSeekGame() {
  const [gameState, setGameState] = useState('welcome');
  const [worldSize, setWorldSize] = useState(2);
  const [playerRole, setPlayerRole] = useState(null);
  const [gameWorld, setGameWorld] = useState([]);
  const [playerMove, setPlayerMove] = useState(null);
  const [computerMove, setComputerMove] = useState(null);
  const [roundResult, setRoundResult] = useState(null);
  const [playerScore, setPlayerScore] = useState(0);
  const [computerScore, setComputerScore] = useState(0);
  const [roundsPlayed, setRoundsPlayed] = useState(0);
  const [showSimulation, setShowSimulation] = useState(false);
  const [simulationResults, setSimulationResults] = useState({
    playerWins: 0,
    computerWins: 0,
    playerScore: 0,
    computerScore: 0,
    totalRounds: 0
  });
  const [isPlayClicked, setIsPlayClicked] = useState(false);

  const placeTypeLabels = ['Neutral', 'Easy for Seeker', 'Hard for Seeker'];
  const placeTypeColors = ['gameworld-label-neutral', 'gameworld-label-easy', 'gameworld-label-hard'];

  const handleSizeChange = (e) => {
    const size = parseInt(e.target.value);
    if (size >= 1) {
      setWorldSize(size);
    }
  };

  const resetGame = async () => {
    setPlayerMove(null);
    setComputerMove(null);
    setRoundResult(null);
    setPlayerScore(0);
    setComputerScore(0);
    setRoundsPlayed(0);
    setShowSimulation(false);
    setIsPlayClicked(false);
  };

  const backToStartPage = () => {
    setGameState('welcome');
    setPlayerRole(null);
    setPlayerMove(null);
    setComputerMove(null);
    setRoundResult(null);
    setPlayerScore(0);
    setComputerScore(0);
    setRoundsPlayed(0);
    setShowSimulation(false);
    setIsPlayClicked(false);
  };

  const startGame = async (role) => {
    setPlayerRole(role);
    setGameWorld(Array(worldSize).fill(0));
    setPlayerMove(null);
    setComputerMove(null);
    setRoundResult(null);
    setIsPlayClicked(false);
    setShowSimulation(false);
    setPlayerScore(0);
    setComputerScore(0);
    setRoundsPlayed(0);
    setGameState('game');
  };

  const selectPlayerMove = (position) => {
    setPlayerMove(position);
    setIsPlayClicked(false);
  };

 
  const playRound = async () => {
    if (playerMove === null) return;
    setIsPlayClicked(true);


    const payload = {
      worldSize,
      playerRole,
      playerMove,
    };


    // const response = await fetch('/api/play', {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify(payload)
    // });

    // const data = await response.json();

    // Update all relevant state from backend response
    // Mock data for testing
    const data = {
      gameWorld: [0, 1, 2],
      computerMove: 1,
      roundResult: { winner: 'a', score: 1 },
      playerScore: playerScore + 1,
      computerScore,
      roundsPlayed: roundsPlayed + 1
    };
    setGameWorld(data.gameWorld);
    setComputerMove(data.computerMove);
    setRoundResult(data.roundResult);
    setPlayerScore(data.playerScore);
    setComputerScore(data.computerScore);
    setRoundsPlayed(data.roundsPlayed);
  };

  const nextRound = async () => {
    setPlayerMove(null);
    setComputerMove(null);
    setRoundResult(null);
    setIsPlayClicked(false);
  };

  const runSimulation = async () => {
    // connect to backend and run simulation
    // setSimulationResults(results);
    setShowSimulation(true);
  };

  if (gameState === 'welcome') {
    return (
      <WelcomeScreen
        worldSize={worldSize}
        onSizeChange={handleSizeChange}
        onStartGame={startGame}
      />
    );
  }

  return (
    <div className="hideandseek-container">
      <div className="hideandseek-gamebox">
        <div className="hideandseek-header">
          <h1 className="hideandseek-title">Hide & Seek Game</h1>
          <div className="hideandseek-roundinfo">
            <span>Round: {roundsPlayed + 1}</span>
            <button
              onClick={resetGame}
              className="hideandseek-resetbtn"
            >
              Reset Game
            </button>
            <button
              onClick={backToStartPage}
              className="hideandseek-resetbtn"
              style={{ marginLeft: '0.5rem' }}
            >
              Back to Start Page
            </button>
          </div>
        </div>

        <ScoreBoard
          playerRole={playerRole}
          playerScore={playerScore}
          computerScore={computerScore}
        />

        <GameWorld
          gameWorld={gameWorld}
          playerMove={playerMove}
          computerMove={isPlayClicked ? computerMove : null}
          placeTypeLabels={placeTypeLabels}
          placeTypeColors={placeTypeColors}
          onPlaceClick={selectPlayerMove}
          playerRole={playerRole}
          showResult={isPlayClicked}
        />

        {roundResult && (
          <div>
            <RoundResult
              roundResult={roundResult}
              onNextRound={nextRound}
            />
          </div>
        )}

        {!roundResult && (
          <>
            {playerMove===null && (
              <div className="hideandseek-prompt">
                <p>Choose a place to {playerRole === 'hider' ? 'hide' : 'seek'}!</p>
              </div>
            )}
            {playerMove !== null && !isPlayClicked && (
              <div className="hideandseek-playbtn-container">
                <button
                  onClick={playRound}
                  className="hideandseek-playbtn"
                >
                  Play
                </button>
              </div>
            )}
          </>
        )}

        <div className="hideandseek-simulation">
          <button
            onClick={runSimulation}
            className="hideandseek-simbtn"
          >
            Run 100 Round Simulation
          </button>
        </div>

        {showSimulation && (
          <SimulationResults simulationResults={simulationResults} />
        )}
      </div>
    </div>
  );
}