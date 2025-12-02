import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/client';
import { Difficulty, Game } from '../api/types';

const CreateGame: React.FC = () => {
  const [difficulty, setDifficulty] = useState<Difficulty>('easy');
  const [player, setPlayer] = useState('');
  const [customRows, setCustomRows] = useState(8);
  const [customCols, setCustomCols] = useState(8);
  const [customTarget, setCustomTarget] = useState(40);
  const [itemsCount, setItemsCount] = useState(6);
  const [oneSwapReset, setOneSwapReset] = useState(false);
  const [randomItemMode, setRandomItemMode] = useState(false);
  const [randomItem, setRandomItem] = useState('');
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const create = async () => {
    try {
      setError(null);
      if (itemsCount < 2 || itemsCount > 100) {
        setError('Items count must be between 2 and 100');
        return;
      }
      const payload: any = { difficulty, player: player.trim() };
      if (difficulty === 'custom') {
        payload.custom = {
          rows: customRows,
          cols: customCols,
          target_score: customTarget,
          items_count: itemsCount,
          one_swap_reset: oneSwapReset,
          random_item_mode: randomItemMode,
          random_item: randomItemMode && randomItem.trim() ? randomItem.trim() : null,
        };
      }
      const { data } = await api.post<Game>('/games', payload);
      navigate(`/game/${data.id}`);
    } catch (e: any) {
      setError(e.response?.data?.detail || 'Failed to create game');
    }
  };

  return (
    <section>
      <h2>New Game</h2>
      <label>
        Nickname:
        <input
          type="text"
          value={player}
          onChange={(e) => setPlayer(e.target.value)}
          placeholder="Enter your nickname"
        />
      </label>
      <label>
        Difficulty:
        <select value={difficulty} onChange={(e) => setDifficulty(e.target.value as Difficulty)}>
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
          <option value="custom">Custom</option>
        </select>
      </label>
      {difficulty === 'custom' && (
        <div className="custom-grid">
          <label>
            Rows
            <input
              type="number"
              value={customRows}
              min={3}
              onChange={(e) => setCustomRows(Number(e.target.value))}
            />
          </label>
          <label>
            Cols
            <input
              type="number"
              value={customCols}
              min={3}
              onChange={(e) => setCustomCols(Number(e.target.value))}
            />
          </label>
          <label>
            Target score
            <input type="number" value={customTarget} onChange={(e) => setCustomTarget(Number(e.target.value))} />
          </label>
          <label>
            Items count
            <input
              type="number"
              value={itemsCount}
              min={3}
              max={100}
              onChange={(e) => setItemsCount(Number(e.target.value))}
            />
          </label>
          <label className="checkbox">
            <input type="checkbox" checked={oneSwapReset} onChange={(e) => setOneSwapReset(e.target.checked)} />
            <span>One-swap reset (no match → reset with penalty)</span>
          </label>
          <label className="checkbox">
            <input type="checkbox" checked={randomItemMode} onChange={(e) => setRandomItemMode(e.target.checked)} />
            <span>Random item scoring</span>
          </label>
          {randomItemMode && (
            <label>
              Lock to item (optional)
              <input type="text" value={randomItem} maxLength={3} onChange={(e) => setRandomItem(e.target.value)} />
            </label>
          )}
        </div>
      )}
      <button onClick={create} disabled={!player.trim()}>
        Start
      </button>
      {error && <p className="error">{error}</p>}
    </section>
  );
};

export default CreateGame;
