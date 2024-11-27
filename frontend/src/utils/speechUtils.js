// 配置语音合成
export const speechConfig = {
    lang: 'nb-NO',        // 挪威语
    pitch: 1,             // 音高
    rate: 0.9,           // 语速
    volume: 1            // 音量
};

// 配置语音识别
export const recognitionConfig = {
    lang: 'nb-NO',        // 挪威语
    continuous: false,    // 不持续识别
    interimResults: false // 只返回最终结果
};

// 数字处理工具
export const extractNumber = (text) => {
    // 将挪威语数字单词转换为数字
    const numberWords = {
        'en': '1', 'to': '2', 'tre': '3', 'fire': '4',
        'fem': '5', 'seks': '6', 'sju': '7', 'åtte': '8',
        'ni': '9', 'ti': '10'
    };
    
    let processedText = text.toLowerCase();
    
    // 替换数字单词
    Object.entries(numberWords).forEach(([word, num]) => {
        processedText = processedText.replace(new RegExp(word, 'g'), num);
    });
    
    // 提取数字
    const matches = processedText.match(/\d+/g);
    return matches ? parseFloat(matches[0]) : null;
}; 