export const parseFraction = (input) => {
    // 处理分数输入
    if (input.includes('/')) {
        const [numerator, denominator] = input.split('/').map(num => parseFloat(num.trim()));
        if (!isNaN(numerator) && !isNaN(denominator) && denominator !== 0) {
            return numerator / denominator;
        }
    }
    // 处理普通数字输入
    return parseFloat(input);
};

export const formatAnswer = (answer) => {
    // 如果答案是整数，直接返回
    if (Number.isInteger(answer)) {
        return answer.toString();
    }
    
    // 如果是小数，尝试转换为分数
    const tolerance = 0.0001; // 设置误差范围
    for (let denominator = 1; denominator <= 100; denominator++) {
        const numerator = Math.round(answer * denominator);
        if (Math.abs(numerator / denominator - answer) < tolerance) {
            return `${numerator}/${denominator}`;
        }
    }
    
    // 如果无法找到合适的分数表示，返回保留3位小数的数字
    return answer.toFixed(3);
}; 