import axios from 'axios';

const API_URL = 'http://localhost:8000/api/education';

export const educationService = {
    // 语言学习
    getLanguageExercises: async (difficulty) => {
        const response = await axios.get(`${API_URL}/language/exercises`, {
            params: { difficulty }
        });
        return response.data;
    },

    checkLanguageAnswer: async (exerciseId, answer) => {
        const response = await axios.post(`${API_URL}/language/check`, {
            exercise_id: exerciseId,
            answer
        });
        return response.data;
    },

    // 数学游戏
    getMathProblems: async (grade = 1, count = 10) => {
        const response = await axios.get(`${API_URL}/math/problems`, {
            params: { grade, count }
        });
        return response.data;
    },

    checkMathAnswer: async (problem_id, answer) => {
        try {
            const response = await axios.post(`${API_URL}/math/check`, {
                problem_id: problem_id,
                answer: answer
            });
            
            if (response.data.error) {
                throw new Error(response.data.error);
            }
            
            return {
                ...response.data,
                analysis: response.data.analysis || null
            };
        } catch (error) {
            console.error('Error checking math answer:', error);
            if (error.response?.status === 404) {
                throw new Error('Oppgaven ble ikke funnet. Vennligst prøv igjen.');
            }
            throw new Error('Kunne ikke sjekke svaret. Prøv igjen senere.');
        }
    },

    // 知识问答
    getQuizQuestions: async (category) => {
        const response = await axios.get(`${API_URL}/quiz/questions`, {
            params: { category }
        });
        return response.data;
    },

    checkQuizAnswer: async (questionId, answer) => {
        const response = await axios.post(`${API_URL}/quiz/check`, {
            question_id: questionId,
            answer
        });
        return response.data;
    }
}; 