import axios from 'axios';
import Logger from '../utils/logger';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const getAuthHeader = () => {
    const token = localStorage.getItem('token');
    return token ? { 'Authorization': `Bearer ${token}` } : {};
};

export const educationService = {
    // 语言学习
    getLanguageExercises: async (difficulty) => {
        try {
            const response = await axios.get(`${API_URL}/education/language/exercises`, {
                params: { difficulty },
                headers: {
                    ...getAuthHeader(),
                    'Content-Type': 'application/json'
                }
            });
            return response.data;
        } catch (error) {
            console.error('Error getting language exercises:', error);
            throw new Error('Kunne ikke laste øvelser');
        }
    },

    checkLanguageAnswer: async (exerciseId, answer) => {
        try {
            const response = await axios.post(`${API_URL}/education/language/check`, {
                exercise_id: exerciseId,
                answer
            }, {
                headers: {
                    ...getAuthHeader(),
                    'Content-Type': 'application/json'
                }
            });
            return response.data;
        } catch (error) {
            console.error('Error checking language answer:', error);
            throw new Error('Kunne ikke sjekke svaret');
        }
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
            Logger.debug('Requesting explanation:', { question, answer, type, age });
            
            const response = await axios.post(`${API_URL}/education/math/explain`, {
                question: question,
                answer: parseFloat(answer),
                type: type,
                age: parseInt(age)
            }, {
                headers: {
                    ...getAuthHeader(),
                    'Content-Type': 'application/json'
                }
            });
            
            Logger.debug('Explanation response:', response.data);
            return response.data;
        } catch (error) {
            Logger.error('Error getting math explanation:', error);
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

    getProblems: async (age, count, rules = null) => {
        try {
            const params = {
                age,
                count
            };
            
            if (rules && rules.length > 0) {
                params.rules = JSON.stringify(rules);
            }

            const response = await axios.get(`${API_URL}/education/math/problems`, {
                params,
                headers: {
                    ...getAuthHeader(),
                    'Content-Type': 'application/json'
                }
            });

            // 确保返回正确的数据结构
            if (response.data && response.data.problems) {
                // 保存批次ID
                if (response.data.batch_id) {
                    localStorage.setItem('currentBatchId', response.data.batch_id);
                }
                return response.data.problems;  // 返回题目数组
            } else {
                console.error('Invalid response format:', response.data);
                return [];
            }
        } catch (error) {
            console.error('Error getting problems:', error);
            throw error;
        }
    },

    checkAnswer: async (problemId, answer, batchId) => {
        try {
            Logger.debug('Checking answer:', {
                problemId,
                answer,
                batchId
            });
            
            const response = await axios.post(`${API_URL}/education/math/check`, {
                problem_id: problemId,
                answer: parseFloat(answer),
                batch_id: batchId
            }, {
                headers: {
                    ...getAuthHeader(),
                    'Content-Type': 'application/json'
                }
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
            
            const response = await axios.get(`${API_URL}/education/math/problems/${batchId}/remaining`, {
                headers: {
                    ...getAuthHeader(),
                    'Content-Type': 'application/json'
                }
            });
            
            // 如果没有找到批次，重新获取题目
            if (!response.data || response.data.length === 0) {
                Logger.debug('No remaining problems found, fetching new problems');
                const newProblems = await educationService.getProblems(
                    localStorage.getItem('currentAge'),
                    localStorage.getItem('currentCount')
                );
                return newProblems;
            }
            
            return response.data;
        } catch (error) {
            Logger.error('Error getting remaining problems:', error);
            return [];
        }
    }
}; 