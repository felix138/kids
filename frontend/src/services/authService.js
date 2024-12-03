import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://192.168.1.40:8000/api';

export const authService = {
    login: async (credentials) => {
        try {
            const formData = new URLSearchParams();
            formData.append('username', credentials.username);
            formData.append('password', credentials.password);

            const response = await fetch(`${API_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData,
                credentials: 'include'
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Pålogging mislyktes');
            }

            const data = await response.json();
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('user', JSON.stringify(data.user));
            return data;
        } catch (error) {
            console.error('Login error:', error);
            throw new Error(error.message || 'Kunne ikke logge inn. Prøv igjen senere.');
        }
    },

    register: async (userData) => {
        try {
            console.log('Sending registration request:', {
                url: `${API_URL}/auth/register`,
                data: userData
            });

            const response = await fetch(`${API_URL}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData),
                credentials: 'include'
            }).catch(error => {
                console.error('Network error:', error);
                throw new Error('Kunne ikke koble til serveren. Sjekk nettverkstilkoblingen.');
            });

            console.log('Registration response:', response);

            if (!response.ok) {
                const errorData = await response.json();
                console.error('Registration error:', errorData);
                throw new Error(errorData.detail || 'Registration failed');
            }

            return await response.json();
        } catch (error) {
            console.error('Registration error:', error);
            throw error;
        }
    },

    logout: () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
    },

    getCurrentUser: () => {
        const userStr = localStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    }
}; 