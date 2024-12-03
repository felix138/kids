import React from 'react';
import { useAuth } from '../../contexts/AuthContext';

function AuthStatus() {
    const { user } = useAuth();

    if (!user) {
        return null;
    }

    return (
        <div className="bg-blue-100 p-2 text-sm text-blue-800 rounded">
            <p>
                Innlogget som: <span className="font-bold">{user.username}</span>
                {user.role && (
                    <span className="ml-2 px-2 py-1 bg-blue-200 rounded text-xs">
                        {user.role}
                    </span>
                )}
            </p>
        </div>
    );
}

export default AuthStatus; 