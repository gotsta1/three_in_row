import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api/client';
import { Game, Snapshot, Direction } from '../api/types';
import Board from '../components/Board';
import Controls from '../components/Controls';
import SnapshotStepper from '../components/SnapshotStepper';

const GamePage: React.FC = () => {
  const { id } = useParams();
  const [game, setGame] = useState<Game | null>(null);
  const [snapshots, setSnapshots] = useState<Snapshot[]>([]);
  const [selectedCell, setSelectedCell] = useState<[number, number] | null>(null);
  const [error, setError] = useState<string | null>(null);

  const loadGame = async () => {
    try {
      const { data } = await api.get<Game>(`/games/${id}`);
      setGame(data);
    } catch (e: any) {
      setError(e.response?.data?.detail || 'Failed to load game');
    }
  };

  useEffect(() => {
    loadGame();
  }, [id]);

  const doSwap = async (direction: Direction) => {
    if (!id || !selectedCell) return;
    try {
      setError(null);
      const { data } = await api.post<Snapshot[]>(`/games/${id}/swap`, {
        row: selectedCell[0],
        col: selectedCell[1],
        direction,
      });
      setSnapshots(data);
      await loadGame();
    } catch (e: any) {
      setError(e.response?.data?.detail || 'Swap failed');
    }
  };

  const resetBoard = async () => {
    if (!id) return;
    try {
      const { data } = await api.post<Snapshot>(`/games/${id}/reset`, {});
      setSnapshots([data]);
      await loadGame();
    } catch (e: any) {
      setError(e.response?.data?.detail || 'Reset failed');
    }
  };

  if (!game) return <p>Loading...</p>;

  return (
    <section>
      <h2>Game {game.id}</h2>
      <p>
        Difficulty: {game.difficulty} | Score: {game.score}/{game.target_score} | Status: {game.status}
        {game.random_item ? ` | Random item: ${game.random_item}` : ''}
        {game.player ? ` | Player: ${game.player}` : ''}
      </p>
      <Board board={game.board} onCellClick={(r, c) => setSelectedCell([r, c])} />
      <p>Selected: {selectedCell ? `${selectedCell[0]},${selectedCell[1]}` : 'none'}</p>
      <Controls onSwap={doSwap} onReset={resetBoard} />
      {snapshots.length > 0 && (
        <div>
          <h3>Snapshots</h3>
          <SnapshotStepper snapshots={snapshots} />
        </div>
      )}
      {error && <p className="error">{error}</p>}
    </section>
  );
};

export default GamePage;
