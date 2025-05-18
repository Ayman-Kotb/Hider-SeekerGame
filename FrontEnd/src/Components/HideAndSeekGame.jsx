import { useState } from 'react';
import WelcomeScreen from './WelcomePage/WelcomeScreen';
import ScoreBoard from './ScoreBoard/ScoreBoard';
import GameWorld from './Game/GameWorld';
import RoundResult from './Results/RoundResult';
import SimulationResults from './Results/SimulationResults';
import './HideAndSeekGame.css';

export default function HideAndSeekGame() {
  const [gameState, setGameState] = useState('welcome');
  const [worldMode, setWorldMode] = useState('linear');
  const [worldSize, setWorldSize] = useState(2);
  const [rows, setRow] = useState(2);
  const [cols, setCol] = useState(2);
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

  const handleRowsChange = (val) => {
    if (val >= 1) {
      setRow(val);
    }
  };
  const handleColsChange = (val) => {
    if (val >= 1) {
      setCol(val);
    }
  };

  const resetGame = async () => {
    try{
      const response = await fetch('http://localhost:5000/api/reset-game', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      const data = await response.json();
      console.log('Game reset:', data);
      setPlayerMove(null);
      setComputerMove(null);
      setRoundResult(null);
      setPlayerScore(0);
      setComputerScore(0);
      setRoundsPlayed(0);
      setShowSimulation(false);
      setIsPlayClicked(false);
    }
    catch (error) {
      console.error('Error resetting game:', error);
    }
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
    setGameWorld([]);
    setWorldSize(2);
    setRow(2);
    setCol(2);
    setWorldMode('linear');
    setSimulationResults({
      playerWins: 0,
      computerWins: 0,
      playerScore: 0,
      computerScore: 0,
      totalRounds: 0
    });
  };

  const startGame = async (role) => {
    setPlayerRole(role);
  const payload = {
    rows: worldMode === 'linear'?1:rows,
    cols: worldMode === 'linear'?worldSize:cols,
    gameMode: 'human', 
    playerRole: role 
  };
try{
  const response = await fetch('http://localhost:5000/api/start-game', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  console.log('Game started:', data);
  setGameWorld(data.gameWorld);
   setPlayerMove(null);
    setComputerMove(null);
    setRoundResult(null);
    setIsPlayClicked(false);
    setShowSimulation(false);
    setPlayerScore(0);
    setComputerScore(0);
    setRoundsPlayed(0);
    setGameState('game');

}catch (error) {
  console.error('Error starting game:', error);
} 
  };

  const selectPlayerMove = (position) => {
    setPlayerMove(position);
    setIsPlayClicked(false);
  };

 
  const playRound = async () => {
    if (playerMove === null) return;
    setIsPlayClicked(true);

    const payload = {
        playerRole: playerRole,
        playerMove: playerMove
    };

    try {
        const response = await fetch('http://localhost:5000/api/play-round', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });
        const data = await response.json();
        console.log('Round played:', data);
        setComputerMove(data.computerMove);
        if(playerRole === 'hider'){
            setPlayerScore(prev => prev + data.hiderScore);
            setComputerScore(prev => prev + data.seekerScore);
             if(data.hiderScore > data.seekerScore)setRoundResult({ winner: 'player', score: data.hiderScore });
             else setRoundResult({ winner: 'computer', score: data.seekerScore }); }     
        else{
          setPlayerScore(prev => prev + data.hiderScore);
          setComputerScore(prev => prev + data.seekerScore);
           if(data.hiderScore > data.seekerScore)setRoundResult({ winner: 'computer', score: data.hiderScore });
           else setRoundResult({ winner: 'player', score: data.seekerScore });
          }
         setRoundsPlayed(prev => prev +1);
    }catch (error) {
        console.error('Error playing round:', error);
    }
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
         rows={rows}
         handleRowChange={handleRowsChange}  // This was wrong - handleRowsChange instead of handleRowChange
         cols={cols}
         handleColsChange={handleColsChange}
         worldMode={worldMode}
         setWorldMode={setWorldMode}
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
          worldMode ={worldMode}
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