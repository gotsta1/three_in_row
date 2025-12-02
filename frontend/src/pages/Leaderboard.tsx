import React, { useEffect, useState } from 'react';
import api from '../api/client';
import { LeaderboardEntry } from '../api/types';

const LeaderboardPage: React.FC = () => {
  const [rows, setRows] = useState<LeaderboardEntry[]>([]);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    try {
      const { data } = await api.get<{ entries: LeaderboardEntry[] }>('/leaderboard');
      setRows(data.entries);
    } catch (e: any) {
      setError(e.response?.data?.detail || 'Failed to load leaderboard');
    }
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <section>
      <h2>Leaderboard</h2>
      {error && <p className="error">{error}</p>}
      <table>
        <thead>
          <tr>
            <th>Place</th>
            <th>Time (s)</th>
            <th>Score</th>
            <th>Difficulty</th>
            <th>Game</th>
            <th>Player</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r, idx) => (
            <tr key={r.id}>
              <td>{idx + 1}</td>
              <td>{r.duration_seconds}</td>
              <td>{r.score}</td>
              <td>{r.difficulty}</td>
              <td>{r.game_id}</td>
              <td>{r.player || '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
};

export default LeaderboardPage;
