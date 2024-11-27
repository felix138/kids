from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import random
from ..core.grok_client import grok_client
import logging

router = APIRouter()

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 定义不同类型的练习模型
class LanguageExercise(BaseModel):
    id: int
    question: str          # 问题内容
    options: List[str]     # 选项列表
    correct_answer: str    # 正确答案
    difficulty: str        # 难度等级
    category: str         # 类别（如语法、词汇等）

class MathProblem(BaseModel):
    id: int
    question: str
    answer: float
    difficulty: str
    grade: int        # 年级
    type: str        # 'basic', 'word_problem', 'geometry'

class KnowledgeQuiz(BaseModel):
    id: int
    question: str         # 测验问题
    options: List[str]    # 答案选项
    correct_answer: str   # 正确答案
    category: str         # 类别（文化、自然、科学）

class MathAnswerRequest(BaseModel):
    problem_id: int
    answer: float

# 语言练习API端点
@router.get("/language/exercises", response_model=List[LanguageExercise])
async def get_language_exercises(difficulty: Optional[str] = None):
    # 示例数据
    exercises = [
        {
            "id": 1,
            "question": "Hvilken setning er grammatisk korrekt?",  # 哪个句子语法正确？
            "options": [
                "Jeg liker å lese bøker",     # 我喜欢读书
                "Jeg liker lese bøker",       # 错误语法
                "Jeg like å lese bøker"       # 错误语法
            ],
            "correct_answer": "Jeg liker å lese bøker",
            "difficulty": "beginner",
            "category": "grammar"
        }
    ]
    return exercises

# 更新数学问题API端点
@router.get("/math/problems", response_model=List[MathProblem])
async def get_math_problems(grade: int = 1, count: int = 10):
    """获取数学题目，可以指定年级和数量"""
    if count > 100:
        raise HTTPException(status_code=400, detail="Maksimalt 100 oppgaver er tillatt")
    
    try:
        # 调用异步函数并等待结果
        problems = await generate_math_problems(grade, count)
        if not problems:
            # 如果没有从Grok获取到题目，使用备用题目
            problems = generate_fallback_problems(grade, count)
        return problems
    except Exception as e:
        print(f"Error generating problems: {e}")
        # 返回备用题目
        return generate_fallback_problems(grade, count)

def generate_fallback_problems(grade: int, count: int) -> List[dict]:
    """生成备用题目"""
    problems = []
    for i in range(count):
        if grade == 1:
            # 1年级：加减法，数字范围1-20
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            op = random.choice(['+', '-'])
            if op == '+':
                answer = num1 + num2
                question = f"{num1} + {num2} = ?"
            else:
                # 确保减法结果为正数
                if num1 < num2:
                    num1, num2 = num2, num1
                answer = num1 - num2
                question = f"{num1} - {num2} = ?"
        
        elif grade == 2:
            # 2年级：加减乘，数字范围1-100
            op = random.choice(['+', '-', '*'])
            if op == '*':
                num1 = random.randint(1, 10)
                num2 = random.randint(1, 10)
            else:
                num1 = random.randint(1, 50)
                num2 = random.randint(1, 50)
            
            if op == '+':
                answer = num1 + num2
                question = f"{num1} + {num2} = ?"
            elif op == '-':
                if num1 < num2:
                    num1, num2 = num2, num1
                answer = num1 - num2
                question = f"{num1} - {num2} = ?"
            else:
                answer = num1 * num2
                question = f"{num1} × {num2} = ?"
        
        else:
            # 3年级：加减乘除，数字范围1-1000
            op = random.choice(['+', '-', '*', '/'])
            if op in ['*', '/']:
                num1 = random.randint(1, 20)
                num2 = random.randint(1, 10)
            else:
                num1 = random.randint(1, 100)
                num2 = random.randint(1, 100)
            
            if op == '+':
                answer = num1 + num2
                question = f"{num1} + {num2} = ?"
            elif op == '-':
                if num1 < num2:
                    num1, num2 = num2, num1
                answer = num1 - num2
                question = f"{num1} - {num2} = ?"
            elif op == '*':
                answer = num1 * num2
                question = f"{num1} × {num2} = ?"
            else:
                # 确保除法结果为整数
                answer = num1
                question = f"{num1 * num2} ÷ {num2} = ?"
        
        problems.append({
            "id": i + 1,
            "question": question,
            "answer": float(answer),
            "difficulty": "beginner" if grade <= 2 else "intermediate",
            "grade": grade,
            "type": "basic"
        })
    
    return problems

# 知识问答API端点
@router.get("/quiz/questions", response_model=List[KnowledgeQuiz])
async def get_quiz_questions(category: Optional[str] = None):
    # 示例数据
    questions = [
        {
            "id": 1,
            "question": "Hva er Norges nasjonalfugl?",  # 挪威的国鸟是什么？
            "options": ["Fossekall", "Ørn", "Kråke", "Spurv"],  # 河鸟、鹰、乌鸦、麻雀
            "correct_answer": "Fossekall",
            "category": "culture"
        }
    ]
    return questions

# 检查语言答案
@router.post("/language/check")
async def check_language_answer(exercise_id: int, answer: str):
    # TODO: 实现答案检查逻辑
    return {"correct": True, "feedback": "Riktig! Bra jobbet!"}  # 正确！做得好！

# 修改问题缓存的实现
_problem_cache = {}

async def get_problem_from_db(problem_id: int) -> dict:
    """从缓存或生成的问题中获取题目"""
    logger.debug(f"Getting problem {problem_id} from cache: {_problem_cache}")
    return _problem_cache.get(problem_id)

# 更新生成数学题目的函数
async def generate_math_problems(grade: int, count: int = 10) -> List[dict]:
    """生成数学题目并存入缓存"""
    global _problem_cache
    _problem_cache.clear()  # 清除旧的缓存
    problems = []
    
    for i in range(min(count, 100)):
        try:
            # 使用Grok生成题目
            problem_type = random.choice(["basic", "word_problem", "geometry"])
            grok_problem = await grok_client.generate_math_problem(grade, problem_type)
            
            if grok_problem:
                problem = {
                    "id": i + 1,
                    "question": grok_problem["question"],
                    "answer": grok_problem["answer"],
                    "difficulty": "beginner" if grade <= 2 else "intermediate",
                    "grade": grade,
                    "type": problem_type
                }
            else:
                # 如果Grok生成失败，使用备用的本地生成逻辑
                problem = generate_fallback_problem(grade, i + 1)
            
            # 将题目添加到缓存和返回列表
            _problem_cache[problem["id"]] = problem
            problems.append(problem)
            logger.debug(f"Generated problem {problem['id']}: {problem}")
            
        except Exception as e:
            logger.error(f"Error generating problem: {e}")
            problem = generate_fallback_problem(grade, i + 1)
            _problem_cache[problem["id"]] = problem
            problems.append(problem)
    
    logger.debug(f"Problem cache after generation: {_problem_cache}")
    return problems

def generate_fallback_problem(age: int, problem_id: int) -> dict:
    """根据年龄生成备用题目"""
    # 计算大致对应的年级
    grade = age - 6 + 1  # 6岁对应1年级
    
    # 根据年龄调整难度和范围
    if age <= 7:  # 6-7岁
        max_num = 20 if age == 6 else 50
        operations = ['+', '-']
    elif age <= 9:  # 8-9岁
        max_num = 100
        operations = ['+', '-', '*']
    elif age <= 10:  # 10岁
        max_num = 1000
        operations = ['+', '-', '*', '/']
    else:  # 11-12岁
        max_num = 10000
        operations = ['+', '-', '*', '/', 'fraction', 'decimal']

    # 生成题目逻辑
    question = ""  # 初始化question变量
    answer = 0     # 初始化answer变量
    problem_type = "basic"  # 初始化problem_type变量

    if age <= 9:
        # 基础运算
        num1 = random.randint(1, max_num)
        num2 = random.randint(1, max_num)
        op = random.choice(operations)
        
        if op == '+':
            answer = num1 + num2
            question = f"{num1} + {num2} = ?"
        elif op == '-':
            if num1 < num2:
                num1, num2 = num2, num1
            answer = num1 - num2
            question = f"{num1} - {num2} = ?"
        elif op == '*':
            answer = num1 * num2
            question = f"{num1} × {num2} = ?"
        else:  # division
            answer = num1
            question = f"{num1 * num2} ÷ {num2} = ?"
        
    elif age == 10:
        # 添加分数和小数
        problem_type = random.choice(['basic', 'fraction', 'decimal'])
        if problem_type == 'fraction':
            num1 = random.randint(1, 10)
            den1 = random.randint(2, 10)
            question = f"Hva er {num1}/{den1} som desimaltall?"
            answer = num1 / den1
        elif problem_type == 'decimal':
            num1 = round(random.uniform(0.1, 10.0), 1)
            num2 = round(random.uniform(0.1, 10.0), 1)
            answer = round(num1 + num2, 2)
            question = f"{num1} + {num2} = ?"
        else:
            num1 = random.randint(100, 1000)
            num2 = random.randint(100, 1000)
            answer = num1 + num2
            question = f"{num1} + {num2} = ?"
            
    elif age == 11:
        # 添加几何和更复杂的分数
        problem_type = random.choice(['geometry', 'complex_fraction', 'percentage'])
        if problem_type == 'geometry':
            side = random.randint(1, 10)
            question = f"Hva er omkretsen av et kvadrat med sider på {side} cm?"
            answer = side * 4
        else:
            num1 = random.randint(1, 100)
            answer = num1 / 2
            question = f"Hva er halvparten av {num1}?"
            
    else:  # 12岁
        # 添加代数和统计
        problem_type = random.choice(['algebra', 'statistics', 'complex_calculation'])
        numbers = [random.randint(1, 20) for _ in range(5)]
        question = f"Hva er gjennomsnittet av tallene: {', '.join(map(str, numbers))}?"
        answer = sum(numbers) / len(numbers)

    return {
        "id": problem_id,
        "question": question,
        "answer": float(answer),
        "difficulty": get_difficulty_by_age(age),
        "age": age,
        "type": problem_type
    }

def get_difficulty_by_age(age: int) -> str:
    """根据年龄返回难度级别"""
    if age <= 7:
        return "beginner"
    elif age <= 9:
        return "intermediate"
    elif age <= 11:
        return "advanced"
    else:
        return "expert"

# 更新答案检查端点
@router.post("/math/check")
async def check_math_answer(request: MathAnswerRequest):
    try:
        # 从缓存中获取问题
        problem = await get_problem_from_db(request.problem_id)
        if not problem:
            logger.error(f"Problem {request.problem_id} not found in cache")
            raise HTTPException(status_code=404, detail="Oppgave ikke funnet")
        
        logger.debug(f"Checking answer for problem {request.problem_id}")
        logger.debug(f"User answer: {request.answer}, Correct answer: {problem['answer']}")
        
        # 使用本地检查逻辑
        is_correct = abs(float(request.answer) - float(problem['answer'])) < 0.001
        
        # 根据答案生成反馈
        if is_correct:
            feedback = "Riktig! Bra jobbet! 🎉"
        else:
            feedback = f"Ikke riktig. Det riktige svaret er {problem['answer']}. Prøv igjen! 💪"
        
        return {
            "correct": is_correct,
            "feedback": feedback
        }
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in check_math_answer: {e}")
        raise HTTPException(status_code=500, detail="Intern serverfeil")

# 检查知识问答答案
@router.post("/quiz/check")
async def check_quiz_answer(question_id: int, answer: str):
    # TODO: 实现知识问答检查
    return {"correct": True, "feedback": "Riktig svar! Du er flink!"}  # 回答正确！你真棒！ 

@router.post("/math/explain")
async def get_math_explanation(
    question: str,
    answer: float,
    problem_type: str,
    age: int
):
    """获取数学题目的详细解释"""
    try:
        explanation = await grok_client.generate_explanation(
            question, answer, problem_type, age
        )
        return {"explanation": explanation}
    except Exception as e:
        logger.error(f"Error generating explanation: {e}")
        return {"explanation": "Beklager, kunne ikke generere forklaring."}

@router.get("/math/similar")
async def get_similar_problems(
    age: int,
    type: str,
    count: int = 2
):
    """生成相似的题目"""
    try:
        problems = []
        for i in range(count):
            problem = await grok_client.generate_math_problem(age, type)
            if problem:
                problems.append({
                    "id": f"similar_{i+1}",
                    **problem,
                    "age": age,
                    "type": type
                })
        return problems
    except Exception as e:
        logger.error(f"Error generating similar problems: {e}")
        return []