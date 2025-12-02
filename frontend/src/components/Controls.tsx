import React from 'react';
import { Direction } from '../api/types';

interface Props {
  onSwap: (dir: Direction) => void;
  onReset: () => void;
}

const Controls: React.FC<Props> = ({ onSwap, onReset }) => (
  <div className="controls">
    <div className="direction-controls">
      <button className="dir-btn" onClick={() => onSwap('up')}>↑ Up</button>
      <div className="dir-row">
        <button className="dir-btn" onClick={() => onSwap('left')}>← Left</button>
        <button className="dir-btn" onClick={() => onSwap('right')}>Right →</button>
      </div>
      <button className="dir-btn" onClick={() => onSwap('down')}>↓ Down</button>
    </div>
    <button className="reset" onClick={onReset}>Reset board (-5 pts)</button>
  </div>
);

export default Controls;
