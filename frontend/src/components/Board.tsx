import React from 'react';

interface Props {
  board: string[][];
  onCellClick?: (row: number, col: number) => void;
}

const BASE_PALETTE = [
  '#ef476f', '#ffd166', '#06d6a0', '#118ab2', '#9b5de5',
  '#ff9f1c', '#00bcd4', '#8bc34a', '#e91e63', '#ff6f61',
  '#4dd0e1', '#7e57c2', '#fbc02d', '#f06292', '#4caf50',
  '#03a9f4', '#ff7043', '#26a69a', '#d4e157', '#5c6bc0',
];

const toIndex = (value: string) => {
  let idx = 0;
  for (const ch of value) {
    const digit = (ch.toUpperCase().charCodeAt(0) - 64);
    if (digit < 1 || digit > 26) continue;
    idx = idx * 26 + digit;
  }
  return Math.max(0, idx - 1); // zero-based
};

const colorForValue = (value: string | undefined | null) => {
  if (!value) return '#8a9aad';
  const idx = toIndex(value);
  if (idx < BASE_PALETTE.length) {
    return BASE_PALETTE[idx];
  }
  // For large counts, spread hues using golden ratio
  const hue = (idx * 137) % 360;
  return `hsl(${hue}, 70%, 55%)`;
};

const Board: React.FC<Props> = ({ board, onCellClick }) => {
  return (
    <div className="board">
      {board.map((row, rIdx) => (
        <div key={rIdx} className="board-row">
          {row.map((cell, cIdx) => (
            <button
              key={cIdx}
              className="cell"
              title={cell}
              aria-label={cell}
              style={{ backgroundColor: colorForValue(cell) }}
              onClick={() => onCellClick?.(rIdx, cIdx)}
            >
              <span className="cell-label">{cell}</span>
            </button>
          ))}
        </div>
      ))}
    </div>
  );
};

export default Board;
