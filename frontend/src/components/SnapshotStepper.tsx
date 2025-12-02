import React, { useState } from 'react';
import { Snapshot } from '../api/types';
import Board from './Board';

interface Props {
  snapshots: Snapshot[];
}

const SnapshotStepper: React.FC<Props> = ({ snapshots }) => {
  const [index, setIndex] = useState(0);
  if (!snapshots.length) return null;
  const snap = snapshots[index];
  return (
    <div className="snapshots">
      <div className="snapshot-controls">
        <button onClick={() => setIndex(Math.max(0, index - 1))} disabled={index === 0}>
          Prev
        </button>
        <span>
          Step {index + 1}/{snapshots.length} {snap.reset_applied ? '(reset)' : ''}
        </span>
        <button onClick={() => setIndex(Math.min(snapshots.length - 1, index + 1))} disabled={index === snapshots.length - 1}>
          Next
        </button>
      </div>
      <Board board={snap.board} />
      <div className="meta">Score: {snap.score} | Status: {snap.status}</div>
    </div>
  );
};

export default SnapshotStepper;
