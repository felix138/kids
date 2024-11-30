// 日志级别
const LogLevel = {
    DEBUG: 'debug',
    INFO: 'info',
    WARN: 'warn',
    ERROR: 'error'
};

// 日志配置
const config = {
    enabled: process.env.REACT_APP_DEBUG === 'true',
    level: process.env.REACT_APP_LOG_LEVEL || LogLevel.INFO,
    problemTracking: true  // 题目跟踪
};

class Logger {
    static debug(...args) {
        if (config.enabled && ['debug'].includes(config.level)) {
            console.debug('[DEBUG]', ...args);
        }
    }

    static info(...args) {
        if (config.enabled && ['debug', 'info'].includes(config.level)) {
            console.info('[INFO]', ...args);
        }
    }

    static warn(...args) {
        if (config.enabled && ['debug', 'info', 'warn'].includes(config.level)) {
            console.warn('[WARN]', ...args);
        }
    }

    static error(...args) {
        if (config.enabled) {
            console.error('[ERROR]', ...args);
        }
    }

    // 专门用于跟踪题目和答案
    static trackProblem(action, data) {
        if (config.enabled && config.problemTracking) {
            console.group(`[Problem Tracking] ${action}`);
            console.log('Timestamp:', new Date().toISOString());
            console.log('Data:', data);
            console.groupEnd();
        }
    }
}

export default Logger; 