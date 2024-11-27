import React from 'react';
import { Link, useLocation } from 'react-router-dom';

function Navbar() {
  const location = useLocation();

  return (
    <nav className="bg-blue-500 p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-white text-xl font-bold">
          AI Utdanningsassistent
        </Link>
        <div className="space-x-4">
          <Link 
            to="/education" 
            className={`text-white hover:text-blue-100 ${
              location.pathname === '/education' ? 'font-bold' : ''
            }`}
          >
            Utdanning
          </Link>
          <Link 
            to="/entertainment" 
            className={`text-white hover:text-blue-100 ${
              location.pathname === '/entertainment' ? 'font-bold' : ''
            }`}
          >
            Underholdning
          </Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar; 