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
        try {
            const response = await axios.get(`${API_URL}/math/problems`, {
                params: { grade, count },
                timeout: 10000  // 设置超时时间
            });
            return response.data;
        } catch (error) {
            console.error('Error getting math problems:', error);
            throw new Error('Kunne ikke laste oppgaver. Prøv igjen senere.');
        }
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
    },

    // 添加获取数学解释的方法
    getMathExplanation: async (question, answer, type, age) => {
        try {
            const response = await axios.post(`${API_URL}/math/explain`, {
                question,
                answer,
                type,
                age
            });
            return response.data.explanation;
        } catch (error) {
            console.error('Error getting math explanation:', error);
            return 'Kunne ikke hente forklaring.';
        }
    },

    // 添加获取相似题目的方法
    getSimilarProblems: async (age, problemType, count) => {
        try {
            const response = await axios.get(`${API_URL}/math/similar`, {
                params: { age, type: problemType, count }
            });
            return response.data;
        } catch (error) {
            console.error('Error getting similar problems:', error);
            return [];
        }
    }
}; 