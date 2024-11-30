import axios from 'axios';
import Logger from '../utils/logger';

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
                question: question,
                answer: parseFloat(answer),
                type: type,
                age: parseInt(age)
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
    },

    getProblems: async (age, count) => {
        try {
            Logger.debug('Requesting problems:', { age, count });
            
            const response = await axios.get(`${API_URL}/math/problems`, {
                params: { age, count }
            });
            
            Logger.trackProblem('API Response', {
                rawResponse: response.data,
                batchId: response.data?.batch_id
            });
            
            if (!response.data || typeof response.data !== 'object') {
                Logger.error('Invalid response format:', response.data);
                return [];
            }
            
            const batchId = response.data.batch_id;
            if (batchId) {
                localStorage.setItem('currentBatchId', batchId);
                Logger.debug('Stored batch ID:', batchId);
            }
            
            const problems = response.data.problems || [];
            Logger.trackProblem('Processed Problems', { problems });
            
            return problems;
        } catch (error) {
            Logger.error('Error getting problems:', error);
            return [];
        }
    },

    checkAnswer: async (problemId, answer, batchId) => {
        try {
            Logger.debug('Checking answer:', {
                problemId,
                answer,
                batchId
            });
            
            const response = await axios.post(`${API_URL}/math/check`, {
                problem_id: problemId,
                answer: parseFloat(answer),
                batch_id: batchId
            });
            
            Logger.debug('Check answer response:', response.data);
            
            return {
                correct: response.data.correct,
                feedback: response.data.feedback,
                correctAnswer: response.data.correct_answer
            };
        } catch (error) {
            Logger.error('Error checking answer:', error);
            throw new Error('Kunne ikke sjekke svaret. Prøv igjen senere.');
        }
    },

    getRemainingProblems: async (batchId) => {
        try {
            Logger.debug('Requesting remaining problems for batch:', batchId);
            
            const response = await axios.get(`${API_URL}/math/problems/${batchId}/remaining`);
            Logger.trackProblem('Received Remaining Problems', {
                batchId,
                problems: response.data
            });
            
            return response.data;
            
        } catch (error) {
            Logger.error('Error getting remaining problems:', error);
            return [];
        }
    }
}; 