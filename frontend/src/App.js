import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Education from './pages/Education';
import Entertainment from './pages/Entertainment';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route exact path="/" element={<Home />} />
          <Route path="/education" element={<Education />} />
          <Route path="/entertainment" element={<Entertainment />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App; 