import React from 'react';

function LoadingSpinner() {
    return (
        <div className="flex justify-center items-center h-screen">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
            <span className="ml-3 text-blue-500">Laster...</span>
        </div>
    );
}

export default LoadingSpinner; 