export type Difficulty = 'easy' | 'medium' | 'hard' | 'custom';
export type Direction = 'up' | 'down' | 'left' | 'right';

export interface Game {
  id: string;
  board: string[][];
  score: number;
  status: string;
  target_score: number;
  difficulty: Difficulty;
  random_item?: string | null;
  player: string;
}

export interface Snapshot {
  board: string[][];
  score: number;
  status: string;
  reset_applied?: boolean;
}

export interface LeaderboardEntry {
  id: string;
  game_id: string;
  difficulty: Difficulty;
  duration_seconds: number;
  score: number;
  player?: string | null;
}
