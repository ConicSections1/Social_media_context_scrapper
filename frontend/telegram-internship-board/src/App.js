import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import ResultsPage from './pages/ResultsPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/results" element={<ResultsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
