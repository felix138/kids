import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Velkommen til AI Utdanningsassistent for Barn</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Link to="/education" className="block">
          <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-shadow">
            <h2 className="text-xl font-bold mb-2">Utdanningsmodul</h2>
            <p>Inkluderer språklæring, matematikkspill og kunnskapsquiz</p>
          </div>
        </Link>
        <Link to="/entertainment" className="block">
          <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-shadow">
            <h2 className="text-xl font-bold mb-2">Underholdningsmodul</h2>
            <p>Morsomme interaktive historier og hjernetrim</p>
          </div>
        </Link>
      </div>
    </div>
  );
}

export default Home; 