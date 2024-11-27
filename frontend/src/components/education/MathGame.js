import React, { useState, useEffect } from 'react';
import { educationService } from '../../services/educationService';

function MathGame() {
    // 状态管理
    const [grade, setGrade] = useState(1);
    const [problemCount, setProblemCount] = useState(10);
    const [gameStarted, setGameStarted] = useState(false);
    const [problems, setProblems] = useState([]);
    const [currentProblem, setCurrentProblem] = useState(null);
    const [currentIndex, setCurrentIndex] = useState(0);
    const [userAnswer, setUserAnswer] = useState('');
    const [feedback, setFeedback] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [score, setScore] = useState(0);
    const [speaking, setSpeaking] = useState(false);
    const [listening, setListening] = useState(false);

    // 语音合成
    const speak = (text) => {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'nb-NO';  // 挪威语
            utterance.rate = 0.9;      // 语速
            utterance.pitch = 1;       // 音高
            setSpeaking(true);
            utterance.onend = () => setSpeaking(false);
            window.speechSynthesis.speak(utterance);
        }
    };

    // 语音识别
    const startListening = () => {
        if ('webkitSpeechRecognition' in window) {
            const recognition = new window.webkitSpeechRecognition();
            recognition.lang = 'nb-NO';
            recognition.continuous = false;
            recognition.interimResults = false;

            recognition.onstart = () => setListening(true);
            recognition.onend = () => setListening(false);
            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                // 提取数字
                const number = parseFloat(transcript.replace(/[^0-9.]/g, ''));
                if (!isNaN(number)) {
                    setUserAnswer(number.toString());
                }
            };

            recognition.start();
        }
    };

    // 加载数学题目
    const loadProblems = async () => {
        try {
            setLoading(true);
            const data = await educationService.getMathProblems(grade, problemCount);
            setProblems(data);
            setCurrentProblem(data[0]);
            setGameStarted(true);
            setLoading(false);
        } catch (error) {
            console.error('Feil ved lasting av matematikkoppgaver:', error);
            setError('Kunne ikke laste oppgaver. Prøv igjen senere.');
            setLoading(false);
        }
    };

    // 处理开始游戏
    const handleStartGame = () => {
        loadProblems();
    };

    // 处理答案提交
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!userAnswer) return;

        try {
            const result = await educationService.checkMathAnswer(
                currentProblem.id,
                parseFloat(userAnswer)
            );

            if (result.correct) {
                setScore(score + 1);
                setFeedback(result.feedback);
                speak(result.feedback);
            } else {
                setFeedback(result.feedback);
                speak(result.feedback);
            }

            setTimeout(() => {
                if (currentIndex < problems.length - 1) {
                    setCurrentIndex(currentIndex + 1);
                    setCurrentProblem(problems[currentIndex + 1]);
                    setUserAnswer('');
                    setFeedback('');
                } else {
                    const finalScore = score + (result.correct ? 1 : 0);
                    const finalFeedback = `Gratulerer! Du har fullført alle oppgavene! Din poengsum: ${finalScore}/${problems.length}`;
                    setFeedback(finalFeedback);
                    speak(finalFeedback);
                    setGameStarted(false);
                }
            }, 2000);
        } catch (error) {
            console.error('Error submitting answer:', error);
            setFeedback(error.message || 'Det oppstod en feil. Prøv igjen.');
        }
    };

    // 朗读当前问题
    const readQuestion = () => {
        if (currentProblem?.question) {
            speak(currentProblem.question);
        }
    };

    // 在问题加载时自动朗读
    useEffect(() => {
        if (currentProblem) {
            readQuestion();
        }
    }, [currentProblem]);

    // 游戏设置界面
    if (!gameStarted) {
        return (
            <div className="p-4">
                <h2 className="text-xl font-bold mb-4">Matematikkspill</h2>
                <div className="bg-white p-6 rounded-lg shadow-lg">
                    <div className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700">
                                Velg klassetrinn:
                            </label>
                            <select
                                value={grade}
                                onChange={(e) => setGrade(parseInt(e.target.value))}
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200"
                            >
                                <option value={1}>1. klasse</option>
                                <option value={2}>2. klasse</option>
                                <option value={3}>3. klasse</option>
                            </select>
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">
                                Antall oppgaver (maks 100):
                            </label>
                            <input
                                type="number"
                                min="1"
                                max="100"
                                value={problemCount}
                                onChange={(e) => setProblemCount(Math.min(100, parseInt(e.target.value) || 1))}
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200"
                            />
                        </div>
                        <button
                            onClick={handleStartGame}
                            className="w-full bg-green-500 text-white py-2 rounded hover:bg-green-600 transition-colors"
                        >
                            Start spill
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    // 加载中状态
    if (loading) return (
        <div className="flex justify-center items-center h-64">
            <div className="text-xl">Laster matematikkoppgaver...</div>
        </div>
    );

    // 错误状态
    if (error) return (
        <div className="bg-red-100 p-4 rounded">
            <p className="text-red-700">{error}</p>
            <button 
                className="mt-4 bg-red-500 text-white px-4 py-2 rounded"
                onClick={loadProblems}
            >
                Prøv igjen
            </button>
        </div>
    );

    // 游戏界面
    return (
        <div className="p-4">
            <h2 className="text-xl font-bold mb-4">Matematikkspill - {grade}. klasse</h2>
            <div className="bg-white p-6 rounded-lg shadow-lg">
                <div className="flex justify-between mb-4 text-sm text-gray-600">
                    <div>Oppgave {currentIndex + 1} av {problems.length}</div>
                    <div>Poeng: {score}</div>
                </div>

                <div className="mb-6">
                    <p className="text-lg font-medium">{currentProblem?.question}</p>
                    <button
                        onClick={readQuestion}
                        disabled={speaking}
                        className="mt-2 px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
                    >
                        {speaking ? 'Leser...' : 'Les spørsmål'}
                    </button>
                </div>

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="flex space-x-2">
                        <input
                            type="number"
                            step="any"
                            value={userAnswer}
                            onChange={(e) => setUserAnswer(e.target.value)}
                            className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                            placeholder="Skriv inn ditt svar..."
                        />
                        <button
                            type="button"
                            onClick={startListening}
                            disabled={listening}
                            className={`px-4 py-2 rounded ${
                                listening 
                                    ? 'bg-red-500'
                                    : 'bg-green-500 hover:bg-green-600'
                            } text-white disabled:opacity-50`}
                        >
                            {listening ? 'Lytter...' : 'Snakk'}
                        </button>
                    </div>
                    <button
                        type="submit"
                        className="w-full bg-green-500 text-white py-2 rounded hover:bg-green-600 transition-colors"
                    >
                        Svar
                    </button>
                </form>

                {feedback && (
                    <div className={`mt-4 p-3 rounded text-center ${
                        feedback.includes('Riktig') || feedback.includes('Gratulerer')
                            ? 'bg-green-100 text-green-700'
                            : 'bg-yellow-100 text-yellow-700'
                    }`}>
                        {feedback}
                    </div>
                )}
            </div>
        </div>
    );
}

export default MathGame; 