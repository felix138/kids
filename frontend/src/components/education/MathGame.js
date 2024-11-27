import React, { useState, useEffect } from 'react';
import { educationService } from '../../services/educationService';
import { parseFraction, formatAnswer } from '../../utils/mathUtils';

function MathGame() {
    // 状态管理
    const [grade, setGrade] = useState(6);
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
    const [showHint, setShowHint] = useState(false);
    const [hint, setHint] = useState('');
    const [canMoveNext, setCanMoveNext] = useState(true);  // 是否可以进入下一题
    const [explanation, setExplanation] = useState('');    // 问题解释
    const [lastWrongType, setLastWrongType] = useState(null); // 上次错误的题目类型
    const [isGenerating, setIsGenerating] = useState(false);  // 添加生成状态
    const [loadedCount, setLoadedCount] = useState(0);        // 已加载题目数量

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
            recognition.lang = 'nb-NO';  // 挪威语
            recognition.continuous = false;
            recognition.interimResults = false;

            recognition.onstart = () => {
                setListening(true);
                setFeedback('Jeg lytter...');  // "我在听..."
            };

            recognition.onend = () => {
                setListening(false);
                setFeedback('');
            };

            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                console.log('完整语音内容:', transcript);  // 记录完整内容
                
                // 先显示完整的语音内容
                setUserAnswer(transcript);

                // 然后尝试提取数字
                const numberWords = {
                    'en': '1', 'ett': '1', 'én': '1',
                    'to': '2', 'tre': '3', 'fire': '4',
                    'fem': '5', 'seks': '6', 'syv': '7',
                    'åtte': '8', 'ni': '9', 'ti': '10',
                    'elleve': '11', 'tolv': '12', 'tretten': '13',
                    'fjorten': '14', 'femten': '15', 'seksten': '16',
                    'sytten': '17', 'atten': '18', 'nitten': '19',
                    'tjue': '20', 'tredve': '30', 'førti': '40',
                    'femti': '50', 'seksti': '60', 'sytti': '70',
                    'åtti': '80', 'nitti': '90', 'hundre': '100'
                };

                // 延迟处理数字，让用户先看到完整内容
                setTimeout(() => {
                    let processedText = transcript.toLowerCase();

                    // 处理分数表达式
                    if (processedText.includes('delt på') || processedText.includes('over')) {
                        const parts = processedText.split(/delt på|over/);
                        if (parts.length === 2) {
                            let num1 = parts[0].trim();
                            let num2 = parts[1].trim();

                            // 转换数字单词
                            Object.entries(numberWords).forEach(([word, num]) => {
                                num1 = num1.replace(new RegExp(`\\b${word}\\b`, 'g'), num);
                                num2 = num2.replace(new RegExp(`\\b${word}\\b`, 'g'), num);
                            });

                            // 提取数字
                            num1 = num1.replace(/[^0-9]/g, '');
                            num2 = num2.replace(/[^0-9]/g, '');

                            if (num1 && num2) {
                                setUserAnswer(`${num1}/${num2}`);
                                setFeedback(`识别为分数: ${num1}/${num2}`);
                                return;
                            }
                        }
                    }

                    // 处理普通数字
                    Object.entries(numberWords).forEach(([word, num]) => {
                        processedText = processedText.replace(new RegExp(`\\b${word}\\b`, 'g'), num);
                    });

                    // 提取数字（包括小数）
                    const number = processedText.match(/\d+([,.]\d+)?/);
                    if (number) {
                        const answer = number[0].replace(',', '.');
                        setUserAnswer(answer);
                        setFeedback(`识别为数字: ${answer}`);
                    } else {
                        setFeedback('未能识别到数字，请重试');
                    }
                }, 1500); // 延迟1.5秒处理
            };

            recognition.onerror = (event) => {
                console.error('语音识别错误:', event.error);
                setListening(false);
                setFeedback('发生错误，请重试');
            };

            recognition.start();
        } else {
            setFeedback('此浏览器不支持语音识别');
        }
    };

    // 加载数学题目
    const loadProblems = async () => {
        try {
            setLoading(true);
            setIsGenerating(true);
            setGameStarted(true);  // 立即开始游戏
            
            // 先生成第一道题目
            const firstProblem = await educationService.getMathProblems(grade, 1);
            setProblems([firstProblem[0]]);
            setCurrentProblem(firstProblem[0]);
            setLoadedCount(1);
            setLoading(false);

            // 在后台继续生成其他题目
            generateRemainingProblems();
        } catch (error) {
            console.error('Feil ved lasting av matematikkoppgaver:', error);
            setError('Kunne ikke laste oppgaver. Prøv igjen senere.');
            setLoading(false);
            setIsGenerating(false);
        }
    };

    // 添加后台生成题目的函数
    const generateRemainingProblems = async () => {
        try {
            const batchSize = 2;  // 每次生成2道题
            for (let i = 1; i < problemCount; i += batchSize) {
                const count = Math.min(batchSize, problemCount - i);
                const newProblems = await educationService.getMathProblems(grade, count);
                setProblems(prev => [...prev, ...newProblems]);
                setLoadedCount(prev => prev + count);
            }
        } catch (error) {
            console.error('Error generating remaining problems:', error);
        } finally {
            setIsGenerating(false);
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
            const parsedAnswer = parseFraction(userAnswer);
            if (isNaN(parsedAnswer)) {
                setFeedback('Ugyldig svar. Prøv igjen!');
                return;
            }

            const result = await educationService.checkMathAnswer(
                currentProblem.id,
                parsedAnswer
            );

            if (result.correct) {
                setScore(score + 1);
                setFeedback(result.feedback);
                speak(result.feedback);
                setCanMoveNext(false);
                setLastWrongType(null);
            } else {
                setLastWrongType(currentProblem.type);
                const correctAnswer = formatAnswer(currentProblem.answer);
                const feedback = `Ikke riktig. Det riktige svaret er ${correctAnswer}.`;
                setFeedback(feedback);
                speak(feedback);
                setCanMoveNext(false);
                
                try {
                    const explanation = await educationService.getMathExplanation(
                        currentProblem.question,
                        parseFloat(correctAnswer),
                        currentProblem.type,
                        currentProblem.age
                    );
                    setExplanation(explanation);
                } catch (error) {
                    console.error('Error getting explanation:', error);
                    setExplanation('Kunne ikke hente forklaring.');
                }
            }

            if (currentIndex >= problems.length - 1) {
                const finalScore = score + (result.correct ? 1 : 0);
                const finalFeedback = `Gratulerer! Du har fullført alle oppgavene! Din poengsum: ${finalScore}/${problems.length}`;
                setFeedback(finalFeedback);
                speak(finalFeedback);
                setGameStarted(false);
            }
        } catch (error) {
            console.error('Error submitting answer:', error);
            setFeedback(error.message || 'Det oppstod en feil. Prøv igjen.');
        }
    };

    // 添加下一题按钮处理函数
    const handleNextProblem = async () => {
        if (currentIndex < problems.length - 1) {
            // 如果上一题答错了，生成两道相似题目
            if (lastWrongType) {
                try {
                    const similarProblems = await educationService.getSimilarProblems(
                        grade,
                        lastWrongType,
                        2
                    );
                    // 插入相似题目到当前位置后
                    problems.splice(currentIndex + 1, 0, ...similarProblems);
                } catch (error) {
                    console.error('Error getting similar problems:', error);
                }
            }
            
            setCurrentIndex(currentIndex + 1);
            setCurrentProblem(problems[currentIndex + 1]);
            setUserAnswer('');
            setFeedback('');
            setExplanation('');
            setCanMoveNext(true);
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

    // 添加提示系统
    const generateHint = () => {
        const problem = currentProblem;
        if (!problem) return;

        let hintText = '';
        if (problem.type === 'percentage') {
            hintText = 'For å finne prosent, del med 100 og gang med prosentsatsen.';
        } else if (problem.type === 'area') {
            hintText = 'Areal = lengde × bredde';
        } else if (problem.type === 'volume') {
            hintText = 'Volum av kube = lengde × bredde × høyde';
        } else if (problem.type === 'fraction') {
            hintText = 'Husk å finne fellesnevner først!';
        } else if (problem.type === 'algebra') {
            hintText = 'Prøv å løse ligningen steg for steg.';
        }
        setHint(hintText);
        setShowHint(true);
    };

    // 游戏设置界面
    if (!gameStarted) {
        return (
            <div className="p-4">
                <h2 className="text-xl font-bold mb-4">Matematikkspill</h2>
                <div className="bg-white p-6 rounded-lg shadow-lg">
                    <div className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700">
                                Velg alder:
                            </label>
                            <select
                                value={grade}
                                onChange={(e) => setGrade(parseInt(e.target.value))}
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200"
                            >
                                <option value={6}>6 år</option>
                                <option value={7}>7 år</option>
                                <option value={8}>8 år</option>
                                <option value={9}>9 år</option>
                                <option value={10}>10 år</option>
                                <option value={11}>11 år</option>
                                <option value={12}>12 år</option>
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
            <h2 className="text-xl font-bold mb-4">Matematikkspill - {grade} år</h2>
            <div className="bg-white p-6 rounded-lg shadow-lg">
                {/* 添加加载进度显示 */}
                {isGenerating && (
                    <div className="mb-4 text-sm text-gray-600">
                        Laster oppgaver: {loadedCount}/{problemCount}
                        <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2">
                            <div 
                                className="bg-blue-600 h-2.5 rounded-full transition-all duration-500"
                                style={{ width: `${(loadedCount/problemCount) * 100}%` }}
                            ></div>
                        </div>
                    </div>
                )}

                <div className="flex justify-between mb-4 text-sm text-gray-600">
                    <div>Oppgave {currentIndex + 1} av {problemCount}</div>
                    <div>Poeng: {score}</div>
                </div>

                <div className="mb-6">
                    <p className="text-lg font-medium">{currentProblem?.question}</p>
                    <div className="flex space-x-2 mt-2">
                        <button
                            onClick={readQuestion}
                            disabled={speaking}
                            className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
                        >
                            {speaking ? 'Leser...' : 'Les spørsmål'}
                        </button>
                        <button
                            onClick={generateHint}
                            className="px-3 py-1 bg-yellow-500 text-white rounded hover:bg-yellow-600"
                        >
                            Vis hint
                        </button>
                    </div>
                    {showHint && hint && (
                        <div className="mt-2 p-2 bg-yellow-100 text-yellow-800 rounded">
                            💡 {hint}
                        </div>
                    )}
                </div>

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="flex space-x-2">
                        <input
                            type="text"
                            value={userAnswer}
                            onChange={(e) => setUserAnswer(e.target.value)}
                            className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                            placeholder="Skriv inn ditt svar (f.eks: 3/8 eller 0.375)..."
                        />
                        <button
                            type="button"
                            onClick={startListening}
                            disabled={listening}
                            className={`px-4 py-2 rounded ${
                                listening 
                                    ? 'bg-red-500 text-white'
                                    : 'bg-green-500 hover:bg-green-600 text-white'
                            } disabled:opacity-50 flex items-center space-x-2`}
                        >
                            {listening ? (
                                <>
                                    <span className="animate-pulse">●</span>
                                    <span>Lytter...</span>
                                </>
                            ) : (
                                <>
                                    <span>🎤</span>
                                    <span>Snakk</span>
                                </>
                            )}
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

                {/* 添加解释部分 */}
                {explanation && (
                    <div className="mt-4 p-4 bg-blue-50 rounded-lg">
                        <h3 className="font-bold mb-2">Forklaring:</h3>
                        <p className="text-gray-700">{explanation}</p>
                    </div>
                )}

                {/* 添加下一题按钮 */}
                {!canMoveNext && (
                    <button
                        onClick={handleNextProblem}
                        className="mt-4 w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 transition-colors"
                    >
                        {currentIndex < problems.length - 1 ? 'Neste oppgave' : 'Avslutt spill'}
                    </button>
                )}
            </div>
        </div>
    );
}

export default MathGame; 