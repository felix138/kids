import React, { useState } from 'react';
import LanguageLearning from '../components/education/LanguageLearning';
import MathGame from '../components/education/MathGame';

function Education() {
  const [activeModule, setActiveModule] = useState(null);

  const renderModule = () => {
    switch (activeModule) {
      case 'language':
        return <LanguageLearning />;
      case 'math':
        return <MathGame />;
      case 'quiz':
        return <div>Kunnskapsquiz kommer snart...</div>;
      default:
        return null;
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Utdanningsmodul</h1>
      
      {!activeModule ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Språklæring */}
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h2 className="text-xl font-bold mb-3">Språklæring</h2>
            <div className="space-y-2">
              <p>• Uttalekorrigering</p>
              <p>• Grammatikkveiledning</p>
              <p>• Ordforrådsøvelser</p>
            </div>
            <button 
              className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
              onClick={() => setActiveModule('language')}
            >
              Start læring
            </button>
          </div>

          {/* Matematikkspill */}
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h2 className="text-xl font-bold mb-3">Matematikkspill</h2>
            <div className="space-y-2">
              <p>• Grunnleggende regning</p>
              <p>• Morsomme tekstoppgaver</p>
              <p>• Geometriforståelse</p>
            </div>
            <button 
              className="mt-4 bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
              onClick={() => setActiveModule('math')}
            >
              Start spill
            </button>
          </div>

          {/* Kunnskapsquiz */}
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h2 className="text-xl font-bold mb-3">Kunnskapsquiz</h2>
            <div className="space-y-2">
              <p>• Norsk kultur</p>
              <p>• Naturkunnskap</p>
              <p>• Vitenskapsutforskning</p>
            </div>
            <button 
              className="mt-4 bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600"
              onClick={() => setActiveModule('quiz')}
            >
              Start utforskning
            </button>
          </div>
        </div>
      ) : (
        <div>
          <button 
            className="mb-4 bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
            onClick={() => setActiveModule(null)}
          >
            ← Tilbake til oversikt
          </button>
          {renderModule()}
        </div>
      )}
    </div>
  );
}

export default Education; 