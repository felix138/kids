import React, { useState, useEffect } from 'react';
import { educationService } from '../../services/educationService';

function LanguageLearning() {
    // 状态管理
    const [exercises, setExercises] = useState([]);          // 所有练习题
    const [currentExercise, setCurrentExercise] = useState(null);  // 当前练习
    const [currentIndex, setCurrentIndex] = useState(0);     // 当前题目索引
    const [feedback, setFeedback] = useState('');           // 反馈信息
    const [loading, setLoading] = useState(true);           // 加载状态
    const [error, setError] = useState(null);               // 错误信息

    // 组件加载时获取练习题
    useEffect(() => {
        loadExercises();
    }, []);

    // 加载练习题
    const loadExercises = async () => {
        try {
            setLoading(true);
            const data = await educationService.getLanguageExercises();
            setExercises(data);
            setCurrentExercise(data[0]);
            setLoading(false);
        } catch (error) {
            console.error('加载练习时出错:', error);
            setError('无���加载练习。请稍后重试。');
            setLoading(false);
        }
    };

    // 处理答案提交
    const handleAnswer = async (answer) => {
        try {
            const result = await educationService.checkLanguageAnswer(
                currentExercise.id,
                answer
            );
            setFeedback(result.feedback);
            
            // 延迟后移动到下一题
            setTimeout(() => {
                if (currentIndex < exercises.length - 1) {
                    setCurrentIndex(currentIndex + 1);
                    setCurrentExercise(exercises[currentIndex + 1]);
                    setFeedback('');
                } else {
                    setFeedback('恭喜！你已完成所有练习！');
                }
            }, 2000);
        } catch (error) {
            console.error('检查答案时出错:', error);
            setFeedback('抱歉，出现错误。请重试。');
        }
    };

    // 加载中状态显示
    if (loading) return (
        <div className="flex justify-center items-center h-64">
            <div className="text-xl">正在加载练习...</div>
        </div>
    );

    // 错误状态显示
    if (error) return (
        <div className="bg-red-100 p-4 rounded">
            <p className="text-red-700">{error}</p>
            <button 
                className="mt-4 bg-red-500 text-white px-4 py-2 rounded"
                onClick={loadExercises}
            >
                重试
            </button>
        </div>
    );

    // 无练习题时显示
    if (!currentExercise) return (
        <div className="text-center">
            <p>暂无可用练习。</p>
        </div>
    );

    // 主要内容渲染
    return (
        <div className="p-4">
            <h2 className="text-xl font-bold mb-4">语言学习</h2>
            <div className="bg-white p-6 rounded-lg shadow-lg">
                {/* 进度显示 */}
                <div className="mb-4 text-sm text-gray-600">
                    练习 {currentIndex + 1} / {exercises.length}
                </div>
                {/* 问题显示 */}
                <p className="mb-4 text-lg">{currentExercise.question}</p>
                {/* 选项列表 */}
                <div className="space-y-2">
                    {currentExercise.options.map((option, index) => (
                        <button
                            key={index}
                            className="w-full p-3 text-left rounded border hover:bg-blue-50 transition-colors"
                            onClick={() => handleAnswer(option)}
                        >
                            {option}
                        </button>
                    ))}
                </div>
                {/* 反馈信息 */}
                {feedback && (
                    <div className={`mt-4 p-3 rounded ${
                        feedback.includes('Riktig') ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                    }`}>
                        {feedback}
                    </div>
                )}
            </div>
        </div>
    );
}

export default LanguageLearning; 