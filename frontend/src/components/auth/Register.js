import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../../services/authService';

function Register() {
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        email: '',
        role: 'student',
        age: ''
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            console.log('Submitting registration:', formData);
            await authService.register(formData);
            console.log('Registration successful');
            navigate('/login');
        } catch (error) {
            console.error('Registration error:', error);
            setError(error.message || 'Det oppstod en feil under registrering');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-purple-500 to-pink-600">
            <div className="bg-white p-8 rounded-lg shadow-xl w-96">
                <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">
                    Registrer deg
                </h2>

                {error && (
                    <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block text-gray-700 mb-2">
                            Brukernavn
                        </label>
                        <input
                            type="text"
                            name="username"
                            value={formData.username}
                            onChange={handleChange}
                            className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-purple-400"
                            required
                        />
                    </div>

                    <div>
                        <label className="block text-gray-700 mb-2">
                            E-post
                        </label>
                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-purple-400"
                            required
                        />
                    </div>

                    <div>
                        <label className="block text-gray-700 mb-2">
                            Passord
                        </label>
                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-purple-400"
                            required
                        />
                    </div>

                    <div>
                        <label className="block text-gray-700 mb-2">
                            Brukertype
                        </label>
                        <select
                            name="role"
                            value={formData.role}
                            onChange={handleChange}
                            className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-purple-400"
                        >
                            <option value="student">Elev</option>
                            <option value="parent">Forelder</option>
                            <option value="admin">Administrator</option>
                        </select>
                    </div>

                    <div>
                        <label className="block text-gray-700 mb-2">
                            Alder (valgfritt)
                        </label>
                        <input
                            type="number"
                            name="age"
                            value={formData.age}
                            onChange={handleChange}
                            className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-purple-400"
                            min="1"
                            max="120"
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className={`w-full py-2 px-4 rounded text-white font-semibold
                            ${loading 
                                ? 'bg-gray-400 cursor-not-allowed' 
                                : 'bg-purple-500 hover:bg-purple-600'}`}
                    >
                        {loading ? 'Registrerer...' : 'Registrer'}
                    </button>
                </form>

                <div className="mt-4 text-center">
                    <p className="text-gray-600">
                        Har du allerede en konto?{' '}
                        <a 
                            href="/login" 
                            className="text-purple-500 hover:text-purple-700"
                        >
                            Logg inn
                        </a>
                    </p>
                </div>
            </div>
        </div>
    );
}

export default Register; 