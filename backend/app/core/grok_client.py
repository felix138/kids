import os
from dotenv import load_dotenv
import aiohttp
import json
import logging

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class GrokClient:
    def __init__(self):
        self.api_key = os.getenv('GROK_API_KEY')
        self.api_base = os.getenv('GROK_API_BASE')
        
        if not self.api_key:
            logger.error("No GROK_API_KEY found in environment variables")
            raise ValueError("GROK_API_KEY environment variable is required")
        
        logger.debug(f"Initialized GrokClient with API base: {self.api_base}")

    async def generate_content(self, prompt: str, count: int = 1) -> str:
        """
        使用 Grok API 生成内容
        
        参数:
            prompt (str): 提示词
            count (int): 需要生成的题目数量
            
        返回:
            str: API 响应内容
        """
        try:
            # 修改提示词，要求返回题目数组
            prompt = f"""Generate {count} math word problems in Norwegian (Bokmål).
            {prompt}
            
            Format the response as JSON array:
            {{
                "problems": [
                    {{
                        "question": "problem text",
                        "answer": numerical_answer,
                        "type": "word_problem",
                        "sub_type": "type"
                    }},
                    ...
                ]
            }}
            """
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'grok-beta',
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': 0.7,
                'max_tokens': 1000
            }
            
            logger.debug("Sending prompt to Grok API:")
            logger.debug("=" * 50)
            logger.debug(prompt)
            logger.debug("=" * 50)
            logger.debug(f"Request data: {data}")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_base,
                    headers=headers,
                    json=data,
                    timeout=30
                ) as response:
                    response_text = await response.text()
                    logger.debug(f"Response status: {response.status}")
                    logger.debug(f"Response text: {response_text}")
                    
                    if response.status == 200:
                        result = json.loads(response_text)
                        content = result['choices'][0]['message']['content']
                        
                        logger.debug("Received response from Grok API:")
                        logger.debug("=" * 50)
                        logger.debug(content)
                        logger.debug("=" * 50)
                        
                        # 处理 Markdown 代码块格式
                        if content.startswith('```') and content.endswith('```'):
                            # 移除 Markdown 代码块标记
                            content = content.replace('```json\n', '').replace('\n```', '')
                            logger.debug("Cleaned content:")
                            logger.debug(content)
                        
                        return content
                    else:
                        logger.error(f"Error from Grok API: {response_text}")
                        raise Exception(f"API returned status {response.status}: {response_text}")
                        
        except Exception as e:
            logger.error(f"Error in generate_content: {e}")
            raise

grok_client = GrokClient() 