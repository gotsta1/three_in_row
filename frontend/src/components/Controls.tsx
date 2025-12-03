import React from 'react';
import { Direction } from '../api/types';

interface Props {
  onSwap: (dir: Direction) => void;
  onReset: () => void;
}

const Controls: React.FC<Props> = ({ onSwap, onReset }) => (
  <div className="controls">
    <div className="direction-controls">
      <button className="dir-btn dir-up" onClick={() => onSwap('up')}>↑ Up</button>
      <button className="dir-btn dir-left" onClick={() => onSwap('left')}>← Left</button>
      <button className="dir-btn dir-right" onClick={() => onSwap('right')}>Right →</button>
      <button className="dir-btn dir-down" onClick={() => onSwap('down')}>↓ Down</button>
    </div>
    <button className="reset" onClick={onReset}>Reset board (-5 pts)</button>
  </div>
);

export default Controls;
