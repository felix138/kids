from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import random
from ..core.grok_client import grok_client
from ..core.logger import logger
from ..core.config import settings
import json
import time
import asyncio
from ..api.auth import get_current_user
from ..models.user import User

router = APIRouter()

# 定义请求模型
class MathAnswerRequest(BaseModel):
    """数学答案请求模型"""
    problem_id: int  # 题目ID
    answer: float    # 用户答案
    batch_id: str    # 添加批次ID

class LanguageExercise(BaseModel):
    id: int
    question: str          # 问题内容
    options: List[str]     # 选项列表
    correct_answer: str    # 正确答案
    difficulty: str        # 难度等级
    category: str         # 类别（如语法、词汇等）

class MathProblem(BaseModel):
    """数学题目模型"""
    id: int         # 题目ID
    question: str   # 题目内容
    answer: float   # 正确答案
    difficulty: str # 难度级别
    age: int       # 适用年龄
    type: str      # 题目类型

class KnowledgeQuiz(BaseModel):
    id: int
    question: str         # 测验问题
    options: List[str]    # 答案选项
    correct_answer: str   # 正确答案
    category: str         # 类别（文化、自然、科学）

class ExplanationRequest(BaseModel):
    question: str
    answer: float
    type: str
    age: int

# 语言练习API端点
@router.get("/language/exercises", response_model=List[LanguageExercise])
async def get_language_exercises(
    difficulty: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    # 示例数据
    exercises = [
        {
            "id": 1,
            "question": "Hvilken setning er grammatisk korrekt?",
            "options": [
                "Jeg liker å lese bøker",
                "Jeg liker lese bøker",
                "Jeg like å lese bøker"
            ],
            "correct_answer": "Jeg liker å lese bøker",
            "difficulty": "beginner",
            "category": "grammar"
        }
    ]
    return exercises

# 修改缓存和状态管理
_problem_cache = {}          # 当前题目缓存
_id_mapping = {}            # ID映射表
_generation_status = {
    'in_progress': False,    # 生成状态
    'total_count': 0,       # 总题目数
    'generated_count': 0,    # 已生成
    'batch_id': None        # 批次ID
}

# 添加批次管理
_batch_problems = {}  # 存储每个批次的题目
_active_batch = None  # 当前活动批次

# 添加响应模型
class MathProblemsResponse(BaseModel):
    batch_id: str
    problems: List[MathProblem]

@router.get("/math/problems", response_model=MathProblemsResponse)
async def get_math_problems(
    age: int = 6, 
    count: int = 10,
    current_user: User = Depends(get_current_user)
):
    """获取数学题目"""
    try:
        logger.info(f"Starting get_math_problems with age={age}, count={count}")
        
        # 生成新的批次ID
        batch_id = str(hash(f"{age}_{count}_{time.time()}"))
        logger.debug(f"Generated batch_id: {batch_id}")
        
        # 创建新的批次存储
        _batch_problems[batch_id] = {}
        
        # 生成初始题目（30%）
        initial_count = max(1, int(count * 0.3))
        logger.debug(f"Will generate {initial_count} initial problems and {count - initial_count} remaining problems")
        
        initial_problems = []
        
        # 生成初始题目
        for i in range(initial_count):
            try:
                problem_id = i + 1
                problem = generate_basic_problem(age, problem_id)
                problem['batch_id'] = batch_id
                problem['id'] = problem_id
                
                # 保存到批次存储
                _batch_problems[batch_id][str(problem_id)] = problem.copy()
                initial_problems.append(problem)
                logger.debug(f"Generated problem {problem_id}: {problem}")
            except Exception as e:
                logger.error(f"Error generating problem {i+1}: {e}")
        
        # 启动异步生成剩余题目
        asyncio.create_task(
            generate_remaining_problems(age, count - initial_count, initial_count, batch_id)
        )
        
        # 确保返回的是有效的响应格式
        response = MathProblemsResponse(
            batch_id=batch_id,
            problems=initial_problems or []
        )
        
        logger.info(f"Returning initial {len(initial_problems)} problems with batch_id {batch_id}")
        return response
        
    except Exception as e:
        logger.error(f"Error in get_math_problems: {e}")
        raise HTTPException(
            status_code=500,
            detail="Kunne ikke generere oppgaver"
        )

async def generate_remaining_problems(age: int, remaining_count: int, start_id: int, batch_id: str):
    """异步生成剩余题目"""
    try:
        # 计算题目分配
        total_count = remaining_count + start_id  # 总题目数
        basic_target = int(total_count * 0.3)    # 基础题目标数量（30%）
        word_target = total_count - basic_target  # 应用题目标数量（70%）
        
        # 计算已有的基础题和应用题数量
        current_basic_count = sum(1 for p in _batch_problems[batch_id].values() 
                                if p.get('type') == 'basic')
        current_word_count = sum(1 for p in _batch_problems[batch_id].values() 
                               if p.get('type') == 'word_problem')
        
        logger.debug(f"Problem generation status: basic={current_basic_count}/{basic_target}, word={current_word_count}/{word_target}")
        
        # 生成应用题（如果需要）
        if current_word_count < word_target:
            try:
                word_count = word_target - current_word_count
                word_problems = await generate_problems_batch(age, word_count)
                logger.debug(f"Generated {len(word_problems)} word problems")
                
                # 为每个应用题添加ID和批次ID
                for i, problem in enumerate(word_problems):
                    problem_id = len(_batch_problems[batch_id]) + 1
                    problem['id'] = problem_id
                    problem['batch_id'] = batch_id
                    problem['difficulty'] = get_difficulty_by_age(age)
                    problem['age'] = age
                    
                    # 保存到批次存储
                    _batch_problems[batch_id][str(problem_id)] = problem.copy()
                    logger.debug(f"Added word problem {problem_id} to batch {batch_id}")
            except Exception as e:
                logger.error(f"Error generating word problems: {e}")
        
        # 生成基础题（如果需要）
        if current_basic_count < basic_target:
            basic_count = basic_target - current_basic_count
            logger.debug(f"Generating {basic_count} basic problems")
            
            for i in range(basic_count):
                try:
                    problem_id = len(_batch_problems[batch_id]) + 1
                    problem = generate_basic_problem(age, problem_id)
                    problem['batch_id'] = batch_id
                    
                    # 保存到批次存储
                    _batch_problems[batch_id][str(problem_id)] = problem.copy()
                    logger.debug(f"Added basic problem {problem_id} to batch {batch_id}")
                except Exception as e:
                    logger.error(f"Error generating basic problem {problem_id}: {e}")
        
        # 记录最终状态
        final_basic_count = sum(1 for p in _batch_problems[batch_id].values() 
                              if p.get('type') == 'basic')
        final_word_count = sum(1 for p in _batch_problems[batch_id].values() 
                             if p.get('type') == 'word_problem')
        
        logger.debug("=== Final Batch Status ===")
        logger.debug(f"Batch ID: {batch_id}")
        logger.debug(f"Total problems: {len(_batch_problems[batch_id])}")
        logger.debug(f"Basic problems: {final_basic_count}/{basic_target}")
        logger.debug(f"Word problems: {final_word_count}/{word_target}")
        
    except Exception as e:
        logger.error(f"Error in generate_remaining_problems: {e}")
        logger.debug(f"Current batch status: {_batch_problems.get(batch_id, {})}")

@router.post("/math/check")
async def check_math_answer(
    request: MathAnswerRequest,
    current_user: User = Depends(get_current_user)
):
    """检查数学答案"""
    try:
        # 添加详细日志
        logger.debug("=== Check Answer Request ===")
        logger.debug(f"Request: {request}")
        logger.debug(f"Available batches: {_batch_problems.keys()}")
        
        # 从对应批次获取题目
        batch = _batch_problems.get(request.batch_id)
        if not batch:
            logger.error(f"Batch {request.batch_id} not found")
            logger.debug(f"All batches: {_batch_problems}")
            raise HTTPException(status_code=404, detail="Invalid batch")
            
        problem = batch.get(str(request.problem_id))
        if not problem:
            logger.error(f"Problem {request.problem_id} not found in batch {request.batch_id}")
            logger.debug(f"Batch contents: {batch}")
            raise HTTPException(status_code=404, detail="Problem not found")
            
        logger.debug(f"Found problem: {problem}")
        logger.debug(f"User answer: {request.answer}")
        
        # 验证答案
        try:
            user_answer = float(request.answer)
            correct_answer = float(problem['answer'])
            
            # 对于基础运算题，直接比较整数值
            if problem['type'] == 'basic':
                user_int = int(user_answer)
                correct_int = int(correct_answer)
                is_correct = user_int == correct_int
                logger.debug(f"Basic problem comparison: {user_int} == {correct_int} -> {is_correct}")
            else:
                # 对于应用题，使用相对误差
                relative_error = abs(user_answer - correct_answer) / abs(correct_answer)
                tolerance = 0.001
                is_correct = relative_error <= tolerance
                logger.debug(f"Word problem comparison: {relative_error} <= {tolerance} -> {is_correct}")
            
            # 生成反馈
            if is_correct:
                feedback = "Riktig! Bra jobbet! 🎉"
            else:
                feedback = f"Ikke riktig. Det riktige svaret er {int(correct_answer) if problem['type'] == 'basic' else correct_answer:.2f}. Prøv igjen! 💪"
            
            response = {
                "correct": is_correct,
                "feedback": feedback,
                "correct_answer": correct_answer
            }
            logger.debug(f"Response: {response}")
            return response
            
        except ValueError as e:
            logger.error(f"Error converting answer to float: {e}")
            raise HTTPException(status_code=400, detail="Ugyldig svar format")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in check_math_answer: {e}")
        raise HTTPException(status_code=500, detail="Error checking answer")

# 知识问答API端点
@router.get("/quiz/questions", response_model=List[KnowledgeQuiz])
async def get_quiz_questions(category: Optional[str] = None):
    # 示例数据
    questions = [
        {
            "id": 1,
            "question": "Hva er Norges nasjonalfugl?",  # 挪的国鸟是什么？
            "options": ["Fossekall", "Ørn", "Kråke", "Spurv"],  # 河鸟、鹰、乌鸦、麻雀
            "correct_answer": "Fossekall",
            "category": "culture"
        }
    ]
    return questions

# 检查语言答案
@router.post("/language/check")
async def check_language_answer(
    exercise_id: int, 
    answer: str,
    current_user: User = Depends(get_current_user)
):
    # TODO: 实现答案检查逻辑
    return {"correct": True, "feedback": "Riktig! Bra jobbet!"}

def generate_basic_problem(age: int, problem_id: int) -> dict:
    """
    生成基础运算题
    
    参数:
        age (int): 学生年龄
        problem_id (int): 题目ID
        
    返回:
        dict: 包含题目信息的字典
    """
    logger.debug(f"Generating basic problem for age {age}, problem_id {problem_id}")
    
    try:
        # 根据年龄设置数字围和运算类型
        if age <= 7:  # 6-7岁
            max_num = 20 if age == 6 else 50
            operations = ['+', '-']  # 仅加减法
        elif age <= 9:  # 8-9岁
            max_num = 100
            operations = ['+', '-', '*']  # 加入乘法
        elif age <= 10:  # 10岁
            max_num = 1000
            operations = ['+', '-', '*', '/']  # 加入除法
        else:  # 11-12岁
            max_num = 10000
            operations = ['+', '-', '*', '/', 'fraction', 'decimal']  # 加入分数和小数

        # 随机选择运算符和生成数字
        op = random.choice(operations)
        
        # 根据运算类型生成合适的数字
        if op == '*':
            num1 = random.randint(1, min(10, max_num))
            num2 = random.randint(1, min(10, max_num))
        elif op == '/':
            num2 = random.randint(1, min(10, max_num))
            answer = random.randint(1, min(10, max_num))
            num1 = num2 * answer  # 确保除法结果为整数
        else:
            num1 = random.randint(1, max_num)
            num2 = random.randint(1, max_num)

        # 生成题目和计算答案
        if op == '+':
            answer = num1 + num2
            question = f"{num1} + {num2} = ?"
        elif op == '-':
            if num1 < num2:  # 确保结果为正数
                num1, num2 = num2, num1
            answer = num1 - num2
            question = f"{num1} - {num2} = ?"
        elif op == '*':
            answer = num1 * num2
            question = f"{num1} × {num2} = ?"
        else:  # division
            answer = num1 / num2
            question = f"{num1} ÷ {num2} = ?"

        return {
            "id": problem_id,
            "question": question,
            "answer": float(answer),
            "difficulty": get_difficulty_by_age(age),
            "age": age,
            "type": "basic"
        }
        
    except Exception as e:
        logger.error(f"Error generating basic problem: {e}")
        # 生成一个简单的加法题作为备用
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        return {
            "id": problem_id,
            "question": f"{num1} + {num2} = ?",
            "answer": float(num1 + num2),
            "difficulty": "beginner",
            "age": age,
            "type": "basic"
        }

def generate_word_problem_sync(age: int) -> dict:
    """同步版本的应用题生成函数"""
    import random
    
    # 根据年龄选择合适的题型
    available_types = []
    if age <= 7:  # 6-7岁
        available_types = ['shopping', 'sharing']
    elif age <= 9:  # 8-9岁
        available_types = ['shopping', 'sharing', 'time']
    else:  # 10岁以上
        available_types = ['shopping', 'sharing', 'time', 'measurement']
    
    problem_type = random.choice(available_types)
    templates = _word_problem_types[problem_type]['templates']
    
    # 根据年龄调整数字范围
    if age <= 7:
        num_range = (1, 20)
    elif age <= 9:
        num_range = (1, 100)
    else:
        num_range = (1, 1000)
    
    # 生成数字
    num1 = random.randint(*num_range)
    num2 = random.randint(*num_range)
    
    # 选择模板和填充内容
    template = random.choice(templates)
    name = random.choice(_norwegian_names)
    
    # 根据题型生成具体问题
    if problem_type == 'shopping':
        item = random.choice(_word_problem_types['shopping']['items'])
        if 'kjøper' in template:
            answer = num1 * num2  # 总价
        else:
            answer = num1 - num2  # 剩余金额
            if answer < 0:  # 确保答案为正数
                num1, num2 = num2, num1
                answer = num1 - num2
    
    elif problem_type == 'sharing':
        item = random.choice(_word_problem_types['sharing']['items'])
        if num2 == 0:  # 避免除零
            num2 = random.randint(1, 5)
        answer = num1 / num2
    
    elif problem_type == 'time':
        place1 = random.choice(_word_problem_types['time']['places'])
        place2 = random.choice(_word_problem_types['time']['places'])
        while place2 == place1:  # 确保两个地点不同
            place2 = random.choice(_word_problem_types['time']['places'])
        time = f"{random.randint(8, 16)}:00"
        answer = num1  # 时间差
    
    elif problem_type == 'measurement':
        if 'areal' in template:  # 面积问题
            answer = num1 * num2
        else:  # 分割问题
            if num2 == 0:  # 避免除以零
                num2 = random.randint(1, 5)
            answer = num1 / num2
    
    # 填充模板
    question = template.format(
        name=name,
        num1=num1,
        num2=num2,
        item=item if 'item' in template else '',
        place1=place1 if 'place1' in template else '',
        place2=place2 if 'place2' in template else '',
        time=time if 'time' in template else ''
    )
    
    return {
        "question": question,
        "answer": float(answer),
        "type": "word_problem",
        "sub_type": problem_type,
        "hash": hash(question),
        "difficulty": get_difficulty_by_age(age),
        "age": age
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

# 添加请求模型
class ExplanationRequest(BaseModel):
    question: str
    answer: float
    type: str
    age: int

@router.post("/math/explain")
async def get_math_explanation(request: ExplanationRequest):
    """获取数学题目的详细解释"""
    
    logger.debug("=== Starting Math Explanation Generation ===")
    logger.debug(f"Request: {request}")
    
    try:
        # 根据题目类型生成不同的解释
        logger.debug(f"Problem type: {request.type}")
        
        if request.type == 'basic':
            logger.debug("Generating basic problem explanation")
            explanation = generate_basic_explanation(request)
            logger.debug(f"Generated basic explanation: {explanation}")
        else:
            logger.debug("Generating word problem explanation")
            explanation = await generate_word_problem_explanation(request)
            logger.debug(f"Generated word problem explanation: {explanation}")
            
        logger.debug("=== Explanation Generation Completed ===")
        return explanation
        
    except Exception as e:
        logger.error(f"Error generating explanation: {e}")
        error_response = {
            'explanation': 'Beklager, kunne ikke generere forklaring.',
            'tips': [
                'Les oppgaven nøye',
                'Finn viktige tall',
                'Tenk på hva du skal finne ut'
            ],
            'example': None
        }
        logger.debug(f"Returning error response: {error_response}")
        return error_response

def generate_basic_explanation(request: ExplanationRequest) -> dict:
    """生成基础运算题的解释"""
    # 解析题目中的运算符和数字
    numbers = [int(n) for n in request.question.split() if n.isdigit()]
    operation = next((op for op in ['+', '-', '×', '÷'] if op in request.question), None)
    
    explanation = {
        '+': f"Når vi legger sammen {numbers[0]} og {numbers[1]}, får vi {request.answer}",
        '-': f"Når vi trekker {numbers[1]} fra {numbers[0]}, får vi {request.answer}",
        '×': f"Når vi ganger {numbers[0]} med {numbers[1]}, får vi {request.answer}",
        '÷': f"Når vi deler {numbers[0]} på {numbers[1]}, får vi {request.answer}"
    }.get(operation, '')

    tips = {
        '+': [
            "Tenk på å telle oppover",
            "Du kan bruke fingre eller tegne streker",
            "Start med det største tallet"
        ],
        '-': [
            "Tenk på å telle nedover",
            "Du kan bruke fingre eller tegne streker",
            "Start med det største tallet"
        ],
        '×': [
            "Tenk på gjentatt addisjon",
            "Du kan bruke gangetabellen",
            f"For eksempel: {numbers[0]} × {numbers[1]} = {numbers[0]} + {numbers[0]} ({numbers[1]} ganger)"
        ],
        '÷': [
            "Tenk på deling i like store grupper",
            "Du kan bruke gjentatt subtraksjon",
            f"For eksempel: {numbers[0]} ÷ {numbers[1]} = hvor mange ganger kan vi trekke fra {numbers[1]}"
        ]
    }.get(operation, [])

    example = {
        '+': f"2 + 3 = 5 (telle oppover: 2, 3, 4, 5)",
        '-': f"5 - 2 = 3 (telle nedover: 5, 4, 3)",
        '×': f"3 × 4 = 12 (3 + 3 + 3 + 3 = 12)",
        '÷': f"12 ÷ 3 = 4 (12 - 3 - 3 - 3 - 3 = 0, vi trakk fra 4 ganger)"
    }.get(operation, None)

    return {
        'explanation': explanation,
        'tips': tips,
        'example': example
    }

async def generate_word_problem_explanation(request: ExplanationRequest) -> dict:
    """生成应用题的解释"""
    prompt = f"""
    Forklar denne oppgaven for et barn ({request.age} år):
    
    Oppgave: {request.question}
    Riktig svar: {request.answer}
    
    Gi:
    1. En enkel forklaring
    2. 3-4 nyttige tips
    3. Et lignende eksempel
    
    Bruk enkelt språk og korte setninger.
    """
    
    try:
        explanation = await grok_client.generate_content(prompt)
        explanation_data = json.loads(explanation)
        
        return {
            'explanation': explanation_data.get('explanation', 'Vi prøver å løse dette steg for steg.'),
            'tips': explanation_data.get('tips', [
                'Les oppgaven nøye',
                'Finn viktige tall',
                'Tenk på hva du skal finne ut'
            ]),
            'example': explanation_data.get('example')
        }
    except Exception as e:
        logger.error(f"Error generating word problem explanation: {e}")
        return {
            'explanation': 'Vi prøver å løse dette steg for steg.',
            'tips': [
                'Les oppgaven nøye',
                'Finn viktige tall',
                'Tenk på hva du skal finne ut'
            ],
            'example': None
        }

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

def create_word_problem_prompt(age: int) -> str:
    """
    建应用题生成提示词
    
    参数:
        age (int): 学生年龄
        
    返回:
        str: 提示词
    """
    # 根据年龄设置题目参数
    if age <= 7:  # 6-7岁
        number_range = {
            "min": 1,
            "max": 20,
            "sum_max": 20
        }
        operations = "only addition and subtraction"
        allowed_types = ["shopping", "sharing"]
        rules = [
            "ONLY use whole numbers (no fractions or decimals)",
            "ONLY use addition and subtraction",
            f"Each number must be between {number_range['min']} and {number_range['max']}",
            f"The sum must not exceed {number_range['sum_max']}",
            "Use simple shopping or sharing scenarios",
            "Ensure final answer is a positive whole number"
        ]
    elif age <= 9:  # 8-9岁
        number_range = {
            "min": 1,
            "max": 100,
            "sum_max": 100
        }
        operations = "addition, subtraction, and simple multiplication"
        allowed_types = ["shopping", "sharing", "time"]
        rules = [
            "Use whole numbers only",
            "Include simple multiplication up to 10",
            f"Numbers must be between {number_range['min']} and {number_range['max']}",
            "Use age-appropriate scenarios"
        ]
    else:  # 10岁以上
        number_range = {
            "min": 1,
            "max": 1000,
            "sum_max": 1000
        }
        operations = "all basic operations"
        allowed_types = ["shopping", "sharing", "time", "measurement"]
        rules = [
            "Can use all basic operations",
            "Can include simple decimals",
            f"Numbers must be between {number_range['min']} and {number_range['max']}",
            "Use real-life scenarios"
        ]

    # 建提示词
    prompt = f"""Generate math word problems in Norwegian (Bokmål) for a {age}-year-old child.

    Age-specific requirements:
    1. This is for a {age}-year-old child
    2. Use numbers in range {number_range['min']}-{number_range['max']}
    3. Only use these operations: {operations}
    4. Problem type must be one of: {', '.join(allowed_types)}

    Rules:
    {chr(10).join('- ' + rule for rule in rules)}

    Format each problem as JSON:
    {{
        "question": "the word problem text",
        "answer": numerical_answer,
        "type": "word_problem",
        "sub_type": "one of: {', '.join(allowed_types)}"
    }}
    """

    return prompt

async def generate_problems_batch(age: int, count: int) -> List[dict]:
    """
    批量成应用题
    
    参数:
        age (int): 学生年龄
        count (int): 需要生成的题目数量
        
    返回:
        List[dict]: 生成的应用题列表
    """
    try:
        # 获取提示词
        prompt = create_word_problem_prompt(age)
        
        # 调用 Grok API 生成题目
        response = await grok_client.generate_content(prompt, count)
        
        # 解析响应
        try:
            problem_data = json.loads(response)
            problems = problem_data.get('problems', [])
            
            # 验证和处理每个题目
            valid_problems = []
            for problem in problems:
                if validate_problem(problem, age):
                    problem['difficulty'] = get_difficulty_by_age(age)
                    problem['age'] = age
                    valid_problems.append(problem)
            
            logger.debug(f"Generated {len(valid_problems)} valid word problems")
            return valid_problems
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Grok API response: {e}")
            return []
            
    except Exception as e:
        logger.error(f"Error in generate_problems_batch: {e}")
        return []

def validate_problem(problem: dict, age: int) -> bool:
    """
    验证生成的题目是否有效
    
    参数:
        problem (dict): 题目数据
        age (int): 学生年龄
        
    返回:
        bool: 题目是否有效
    """
    try:
        # 检查必需字段
        required_fields = ['question', 'answer', 'type', 'sub_type']
        if not all(field in problem for field in required_fields):
            logger.error(f"Missing required fields in problem: {problem}")
            return False
            
        # 检查答案是否为数字
        if not isinstance(problem['answer'], (int, float)):
            logger.error(f"Invalid answer type in problem: {problem}")
            return False
            
        # 根据年龄检查答案范围
        answer = float(problem['answer'])
        if age <= 7:
            if not (0 <= answer <= 20):
                logger.error(f"Answer out of range for age {age}: {answer}")
                return False
        elif age <= 9:
            if not (0 <= answer <= 100):
                logger.error(f"Answer out of range for age {age}: {answer}")
                return False
                
        # 检查题目类型
        valid_types = ['word_problem']
        if problem['type'] not in valid_types:
            logger.error(f"Invalid problem type: {problem['type']}")
            return False
            
        # 检查子类型
        valid_subtypes = ['shopping', 'sharing', 'time', 'measurement']
        if problem['sub_type'] not in valid_subtypes:
            logger.error(f"Invalid problem sub_type: {problem['sub_type']}")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"Error validating problem: {e}")
        return False

@router.get("/math/problems/{batch_id}/remaining", response_model=List[MathProblem])
async def get_remaining_problems(
    batch_id: str,
    current_user: User = Depends(get_current_user)
):
    """获取批次中的剩余题目"""
    try:
        logger.debug(f"Getting remaining problems for batch {batch_id}")
        logger.debug(f"Available batches: {_batch_problems.keys()}")
        
        # 获取批次
        batch = _batch_problems.get(batch_id)
        if not batch:
            logger.error(f"Batch {batch_id} not found")
            raise HTTPException(status_code=404, detail="Invalid batch")
            
        # 获取所有题目
        problems = list(batch.values())
        logger.debug(f"Found {len(problems)} problems in batch")
        
        # 按ID排序
        problems.sort(key=lambda x: x['id'])
        logger.debug(f"Returning problems: {problems}")
        
        return problems
        
    except Exception as e:
        logger.error(f"Error getting remaining problems: {e}")
        raise HTTPException(status_code=500, detail="Could not get remaining problems")