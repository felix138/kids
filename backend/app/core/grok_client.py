import os
from dotenv import load_dotenv
import aiohttp
import json
import logging

load_dotenv()

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 配置Grok API
GROK_API_KEY = os.getenv("GROK_API_KEY", "xai-SIdr7qy50GxzLJHKdXrQ0NEQ8gD4zAacLA3ExH4Uc3mXfApAB2mPvndWSGz2FE8N50o1Q21mGT3jMBEN")
GROK_API_BASE = "https://api.x.ai/v1/chat/completions"

class GrokClient:
    def __init__(self):
        self.api_key = os.getenv("GROK_API_KEY")
        if not self.api_key:
            logger.error("No GROK_API_KEY found in environment variables")
            self.api_key = "xai-SIdr7qy50GxzLJHKdXrQ0NEQ8gD4zAacLA3ExH4Uc3mXfApAB2mPvndWSGz2FE8N50o1Q21mGT3jMBEN"
        
        self.api_base = os.getenv("GROK_API_BASE", "https://api.x.ai/v1/chat/completions")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        logger.debug(f"Initialized GrokClient with API base: {self.api_base}")

    async def generate_math_problem(self, grade: int, problem_type: str) -> dict:
        """使用Grok生成数学题目"""
        try:
            prompt = self._create_math_prompt(grade, problem_type)
            logger.debug(f"Sending prompt to Grok: {prompt}")
            
            payload = {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a math teacher for children. Always respond in Norwegian. Format your response exactly as: 'Question: [question] Answer: [number]'"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "model": "grok-beta",
                "temperature": 0.7,
                "max_tokens": 150
            }
            
            logger.debug(f"Request headers: {self.headers}")
            logger.debug(f"Request payload: {payload}")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_base,
                    headers=self.headers,
                    json=payload
                ) as response:
                    response_text = await response.text()
                    logger.debug(f"Grok API response status: {response.status}")
                    logger.debug(f"Grok API response: {response_text}")
                    
                    if response.status == 200:
                        data = json.loads(response_text)
                        content = data['choices'][0]['message']['content']
                        logger.debug(f"Parsed content: {content}")
                        return self._parse_math_response(content)
                    else:
                        logger.error(f"Error from Grok API: {response.status} - {response_text}")
                        return None
        except Exception as e:
            logger.error(f"Error generating math problem: {str(e)}")
            return None

    async def check_math_answer(self, question: str, user_answer: float, correct_answer: float) -> dict:
        """使用Grok验证数学答案"""
        try:
            payload = {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a math teacher checking answers. Respond in Norwegian. Format: 'Correct: [true/false] Feedback: [explanation]'"
                    },
                    {
                        "role": "user",
                        "content": f"Question: {question}\nStudent's answer: {user_answer}\nCorrect answer: {correct_answer}"
                    }
                ],
                "model": "grok-beta",
                "temperature": 0.7,
                "max_tokens": 150
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_base,
                    headers=self.headers,
                    json=payload
                ) as response:
                    response_text = await response.text()
                    logger.debug(f"Answer check response: {response_text}")
                    
                    if response.status == 200:
                        data = json.loads(response_text)
                        content = data['choices'][0]['message']['content']
                        return self._parse_answer_check(content, user_answer, correct_answer)
                    else:
                        logger.error(f"Error checking answer: {response.status} - {response_text}")
                        return self._fallback_answer_check(user_answer, correct_answer)
        except Exception as e:
            logger.error(f"Error checking answer: {str(e)}")
            return self._fallback_answer_check(user_answer, correct_answer)

    def _create_math_prompt(self, grade: int, problem_type: str) -> str:
        """创建数学题目提示"""
        prompts = {
            1: {
                "basic": "Create a simple addition or subtraction problem for 1st grade with numbers under 20. Format: 'Question: [question] Answer: [number]'",
                "word_problem": "Create a simple word problem with addition for 1st grade. Format: 'Question: [question] Answer: [number]'"
            },
            2: {
                "basic": "Create a multiplication or division problem for 2nd grade with numbers under 100. Format: 'Question: [question] Answer: [number]'",
                "word_problem": "Create a word problem with multiplication for 2nd grade. Format: 'Question: [question] Answer: [number]'"
            },
            3: {
                "basic": "Create a mixed arithmetic problem for 3rd grade with numbers under 1000. Format: 'Question: [question] Answer: [number]'",
                "word_problem": "Create a complex word problem for 3rd grade. Format: 'Question: [question] Answer: [number]'",
                "geometry": "Create a simple geometry problem about perimeter or area for 3rd grade. Format: 'Question: [question] Answer: [number]'"
            }
        }
        return prompts.get(grade, {}).get(problem_type, prompts[1]["basic"])

    def _parse_math_response(self, response: str) -> dict:
        """解析Grok的响应"""
        try:
            logger.debug(f"Parsing response: {response}")
            parts = response.split("Question:", 1)
            if len(parts) < 2:
                logger.error("No 'Question:' found in response")
                return None
            
            question_answer = parts[1].split("Answer:", 1)
            if len(question_answer) < 2:
                logger.error("No 'Answer:' found in response")
                return None
                
            question = question_answer[0].strip()
            answer = float(question_answer[1].strip())
            
            logger.debug(f"Parsed question: {question}")
            logger.debug(f"Parsed answer: {answer}")
            
            return {
                "question": question,
                "answer": answer
            }
        except Exception as e:
            logger.error(f"Error parsing response: {e}")
            logger.error(f"Response was: {response}")
            return None

    def _parse_answer_check(self, response: str, user_answer: float, correct_answer: float) -> dict:
        """解析Grok的答案检查响应"""
        try:
            parts = response.split("Correct:", 1)[1].split("Feedback:", 1)
            is_correct = "true" in parts[0].lower()
            feedback = parts[1].strip()
        except:
            return self._fallback_answer_check(user_answer, correct_answer)
        
        return {
            "correct": is_correct,
            "feedback": feedback
        }

    def _fallback_answer_check(self, user_answer: float, correct_answer: float) -> dict:
        """备用的答案检查逻辑"""
        is_correct = abs(user_answer - correct_answer) < 0.001
        feedback = "Riktig! Bra jobbet! 🎉" if is_correct else "Ikke riktig. Prøv igjen! 💪"
        return {
            "correct": is_correct,
            "feedback": feedback
        }

grok_client = GrokClient() 