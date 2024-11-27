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
        # 从环境变量获取API密钥
        self.api_key = os.getenv("GROK_API_KEY")
        if not self.api_key:
            logger.error("No GROK_API_KEY found in environment variables")
            raise ValueError("GROK_API_KEY environment variable is required")
        
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

    def _create_math_prompt(self, age: int, problem_type: str) -> str:
        """根据年龄创建数学题目提示"""
        base_prompt = (
            f"Create a math problem suitable for a {age}-year-old Norwegian child. "
            f"The child is in grade {age-6+1}. "
            "Format your response exactly as: 'Question: [question in Norwegian] Answer: [number]'"
        )

        age_specific_prompts = {
            6: {
                "basic": base_prompt + " Use numbers under 20, focus on basic addition and subtraction.",
                "word_problem": base_prompt + " Create a simple word problem about everyday situations.",
            },
            7: {
                "basic": base_prompt + " Use numbers under 100, include addition and subtraction.",
                "word_problem": base_prompt + " Create a word problem about shopping or sharing.",
            },
            8: {
                "basic": base_prompt + " Include multiplication tables up to 5, numbers under 100.",
                "word_problem": base_prompt + " Create a word problem involving groups or sets.",
            },
            9: {
                "basic": base_prompt + " Include all multiplication tables and simple division.",
                "word_problem": base_prompt + " Create a word problem about measurements or time.",
            },
            10: {
                "basic": base_prompt + " Include fractions and decimals.",
                "word_problem": base_prompt + " Create a problem about percentages or proportions.",
                "geometry": base_prompt + " Create a problem about area or perimeter."
            },
            11: {
                "basic": base_prompt + " Include more complex fractions and decimals.",
                "word_problem": base_prompt + " Create a multi-step problem.",
                "geometry": base_prompt + " Include problems about volume or angles."
            },
            12: {
                "basic": base_prompt + " Include negative numbers and basic algebra.",
                "word_problem": base_prompt + " Create a problem involving ratios or rates.",
                "geometry": base_prompt + " Include problems about circles or 3D shapes."
            }
        }

        # 获取年龄特定的提示，如果没有则使用基本提示
        age_prompts = age_specific_prompts.get(age, age_specific_prompts[6])
        return age_prompts.get(problem_type, age_prompts["basic"])

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
            answer_str = question_answer[1].strip()
            
            # 清理和标准化答案字符串
            answer_str = ''.join(c for c in answer_str if c.isdigit() or c in '.-,')
            answer_str = answer_str.replace(',', '.')
            
            try:
                answer = float(answer_str)
                # 对于接近整数的答案，转换为整数
                if abs(answer - round(answer)) < 0.001:
                    answer = round(answer)
            except ValueError:
                logger.error(f"Could not convert answer to float: {answer_str}")
                return None
            
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

    async def generate_explanation(
        self,
        question: str,
        answer: float,
        problem_type: str,
        age: int
    ) -> str:
        """生成题目解释"""
        try:
            prompt = (
                f"Explain this math problem to a {age}-year-old Norwegian child:\n"
                f"Problem: {question}\n"
                f"Answer: {answer}\n"
                "Provide a step-by-step explanation in Norwegian, "
                "using simple language and maybe a relevant example."
            )
            
            payload = {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a patient and encouraging math teacher for children."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "model": "grok-beta",
                "temperature": 0.7,
                "max_tokens": 250
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_base,
                    headers=self.headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data['choices'][0]['message']['content']
                    else:
                        return "Beklager, kunne ikke generere forklaring."
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            return "Beklager, kunne ikke generere forklaring."

grok_client = GrokClient() 