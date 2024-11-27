import React from 'react';

function Entertainment() {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Underholdningsmodul</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Interaktive historier */}
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-bold mb-3">Interaktive Historier</h2>
          <div className="space-y-3">
            <p className="text-gray-600">
              Utforsk en spennende historieverden, du kan:
            </p>
            <ul className="list-disc list-inside space-y-2">
              <li>Velg hovedperson</li>
              <li>Bestem historiens utvikling</li>
              <li>Skap din egen slutt</li>
            </ul>
            <button className="mt-4 bg-indigo-500 text-white px-6 py-2 rounded-lg hover:bg-indigo-600">
              Start lesing
            </button>
          </div>
        </div>

        {/* Hjernetrim */}
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-bold mb-3">Hjernetrim</h2>
          <div className="space-y-3">
            <p className="text-gray-600">
              Utfordre tankene dine med:
            </p>
            <ul className="list-disc list-inside space-y-2">
              <li>Morsomme gåter</li>
              <li>Logiske oppgaver</li>
              <li>Hukommelsesspill</li>
            </ul>
            <button className="mt-4 bg-pink-500 text-white px-6 py-2 rounded-lg hover:bg-pink-600">
              Start spill
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Entertainment; 