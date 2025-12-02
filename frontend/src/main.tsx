import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import CreateGame from './pages/CreateGame';
import GamePage from './pages/Game';
import LeaderboardPage from './pages/Leaderboard';
import './styles.css';

const App = () => (
  <BrowserRouter>
    <header className="app-header">
      <h1>Three In Row</h1>
      <nav>
        <Link to="/">Create</Link>
        <Link to="/leaderboard">Leaderboard</Link>
      </nav>
    </header>
    <main className="app-main">
      <Routes>
        <Route path="/" element={<CreateGame />} />
        <Route path="/game/:id" element={<GamePage />} />
        <Route path="/leaderboard" element={<LeaderboardPage />} />
      </Routes>
    </main>
  </BrowserRouter>
);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
