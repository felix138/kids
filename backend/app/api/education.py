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

# 定义请求模型
class MathAnswerRequest(BaseModel):
    problem_id: int
    answer: float

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
    age: int
    type: str

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

# 修改问题缓存的实现
_problem_cache = {}

async def get_problem_from_db(problem_id: int) -> dict:
    """从缓存或生成的问题中获取题目"""
    logger.debug(f"Getting problem {problem_id} from cache: {_problem_cache}")
    return _problem_cache.get(str(problem_id))

# 添加知识点追踪
_knowledge_points = {
    'basic': ['addition', 'subtraction', 'multiplication', 'division'],
    'fraction': ['decimal_conversion', 'fraction_addition', 'fraction_comparison'],
    'geometry': ['area', 'perimeter', 'volume', 'angles'],
    'word_problem': ['money', 'time', 'distance', 'shopping', 'sharing'],
    'decimal': ['decimal_addition', 'decimal_comparison', 'percentage'],
    'statistics': ['mean', 'median', 'mode', 'range']
}

# 添加已使用问题追踪
_used_questions = set()
_used_knowledge_points = {}

async def generate_math_problems(age: int, count: int = 10) -> List[dict]:
    """生成数学题目并存入缓存"""
    global _problem_cache, _used_questions, _used_knowledge_points
    problems = []
    
    # 初始化或重置知识点使用计数
    if not _used_knowledge_points:
        _used_knowledge_points = {k: {p: 0 for p in points} 
                                for k, points in _knowledge_points.items()}
    
    # 获取下一个问题ID
    existing_ids = set(_problem_cache.keys())
    next_id = max([int(id) for id in existing_ids]) + 1 if existing_ids else 1
    
    # 根据年龄调整应用题和基础题的比例
    if age <= 7:
        word_problem_ratio = 0.3  # 30% 应用题
    elif age <= 9:
        word_problem_ratio = 0.5  # 50% 应用题
    else:
        word_problem_ratio = 0.7  # 70% 应用题
    
    word_problem_count = int(count * word_problem_ratio)
    basic_problem_count = count - word_problem_count
    
    for i in range(count):
        try:
            # 决定是生成应用题还是基础题
            if i < word_problem_count:
                # 生成应用题
                problem_data = await generate_word_problem(age)
                if problem_data["hash"] in _used_questions:
                    # 如果题目重复，尝试重新生成
                    for _ in range(3):  # 最多尝试3次
                        problem_data = await generate_word_problem(age)
                        if problem_data["hash"] not in _used_questions:
                            break
                    else:
                        # 如果3次都重复，生成基础题
                        problem_data = generate_fallback_problem(age, next_id + i)
                
                problem = {
                    "id": next_id + i,
                    "question": problem_data["question"],
                    "answer": problem_data["answer"],
                    "difficulty": get_difficulty_by_age(age),
                    "age": age,
                    "type": "word_problem",
                    "sub_type": problem_data.get("sub_type", "basic")
                }
                _used_questions.add(problem_data["hash"])
                
            else:
                # 生成基础运算题
                problem = generate_fallback_problem(age, next_id + i)
                # 确保基础题不重复
                while str(problem["id"]) in _problem_cache:
                    problem = generate_fallback_problem(age, next_id + i + 100)
            
            _problem_cache[str(problem["id"])] = problem
            problems.append(problem)
            
            logger.debug(f"Generated problem {problem['id']}:")
            logger.debug(f"Type: {problem['type']}")
            logger.debug(f"Question: {problem['question']}")
            logger.debug(f"Answer: {problem['answer']}")
            
        except Exception as e:
            logger.error(f"Error generating problem {next_id + i}: {e}")
            problem = generate_fallback_problem(age, next_id + i)
            _problem_cache[str(problem["id"])] = problem
            problems.append(problem)
    
    # 清理过旧的缓存数据
    if len(_used_questions) > 1000:
        _used_questions.clear()
    
    # 随机打乱题目顺序
    random.shuffle(problems)
    
    return problems

def get_min_age_for_type(problem_type: str) -> int:
    """返回每种题型的最小适用年龄"""
    type_age_map = {
        'basic': 6,
        'word_problem': 7,
        'fraction': 9,
        'decimal': 9,
        'geometry': 8,
        'statistics': 11
    }
    return type_age_map.get(problem_type, 6)

@router.get("/math/problems", response_model=List[MathProblem])
async def get_math_problems(grade: int = 1, count: int = 10):
    """获取数学题目，可以指定年级和数量"""
    if count > 100:
        raise HTTPException(status_code=400, detail="Maksimalt 100 oppgaver er tillatt")
    
    try:
        problems = await generate_math_problems(grade, count)
        
        # 验证返回的问题
        logger.debug("Problems being returned to client:")
        for p in problems:
            logger.debug(f"ID: {p['id']}, Question: {p['question']}, Answer: {p['answer']}")
            
        return problems
    except Exception as e:
        logger.error(f"Error in get_math_problems: {e}")
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
            "question": "Hva er Norges nasjonalfugl?",  # 挪的国鸟是什么？
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

def generate_fallback_problem(age: int, problem_id: int) -> dict:
    """根据年龄生成备用题目"""
    import random
    
    # 决定是生成应用题还是基础运算题
    is_word_problem = random.random() < 0.6  # 60%的概率生成应用题
    
    if is_word_problem:
        try:
            # 尝试生成应用题
            problem_data = {
                "id": problem_id,
                **generate_word_problem_sync(age)  # 使用同步版本的应用题生成
            }
            return problem_data
        except Exception as e:
            logger.error(f"Error generating word problem: {e}")
            # 如果应用题生成失败，回退到基础运算题
            is_word_problem = False
    
    if not is_word_problem:
        # 生成基础运算题
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
        
        return {
            "id": problem_id,
            "question": question,
            "answer": float(answer),
            "difficulty": get_difficulty_by_age(age),
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
        if num2 == 0:  # 避免除以零
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

# 更新答案检端点
@router.post("/math/check")
async def check_math_answer(request: MathAnswerRequest):
    """检查数学答案"""
    try:
        # 从缓存中获取问题，使用字符串ID
        problem = await get_problem_from_db(str(request.problem_id))  # 确保使用字符串ID
        if not problem:
            logger.error(f"Problem {request.problem_id} not found in cache")
            raise HTTPException(status_code=404, detail="Oppgave ikke funnet")
        
        logger.debug(f"Checking answer for problem {request.problem_id}")
        logger.debug(f"Problem from cache: {problem}")
        logger.debug(f"User answer: {request.answer}, Correct answer: {problem['answer']}")
        
        # 使用更精确的浮点数比较
        user_answer = float(request.answer)
        correct_answer = float(problem['answer'])
        
        # 根据题目类型调整误差范围
        if problem['type'] in ['word_problem', 'geometry', 'decimal', 'fraction']:
            tolerance = 0.01  # 对于应用题和小数题目使用更大的误差范围
        else:
            tolerance = 0.001  # 对于基础运算题使用更小的误差范围
            
        is_correct = abs(user_answer - correct_answer) <= tolerance
        
        # 根据答案和题目类型生成反馈
        if is_correct:
            feedback = "Riktig! Bra jobbet! 🎉"
            if problem['type'] == 'word_problem':
                feedback += " Du er flink til å løse tekstoppgaver!"  # 你很擅长解决应用题！
        else:
            # 格式化正确答案显示
            if abs(correct_answer - round(correct_answer)) < 0.001:
                # 如果是整数，不显示小数点
                formatted_answer = str(int(correct_answer))
            else:
                # 如果是小数，保留两位小数
                formatted_answer = f"{correct_answer:.2f}"
            
            feedback = f"Ikke riktig. Det riktige svaret er {formatted_answer}. "
            
            # 根据题目类型添加额外提示
            if problem['type'] == 'word_problem':
                feedback += "Les oppgaven nøye og prøv igjen! 💪"  # 仔细阅读题目，再试一次！
            else:
                feedback += "Prøv igjen! 💪"  # 再试一次！
        
        return {
            "correct": is_correct,
            "feedback": feedback,
            "correct_answer": correct_answer
        }
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in check_math_answer: {e}")
        logger.error(f"Request data: {request}")
        raise HTTPException(status_code=500, detail="Intern serverfeil")

# 检查知识问答答案
@router.post("/quiz/check")
async def check_quiz_answer(question_id: int, answer: str):
    # TODO: 实现知识问答检查
    return {"correct": True, "feedback": "Riktig svar! Du er flink!"}  # 回答正确！你真棒！ 

# 添加请求模型
class ExplanationRequest(BaseModel):
    question: str
    answer: float
    type: str
    age: int

@router.post("/math/explain")
async def get_math_explanation(request: ExplanationRequest):
    """获取数学题目的详细解释"""
    try:
        explanation = await grok_client.generate_explanation(
            request.question,
            request.answer,
            request.type,
            request.age
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

# 添加应用题类型
_word_problem_types = {
    'shopping': {
        'templates': [
            "Hvis {name} har {num1} kroner og kjøper {item} for {num2} kroner, hvor mange kroner har {name} igjen?",
            "{name} kjøper {num1} {item} for {num2} kroner hver. Hvor mye må {name} betale totalt?",
            "En {item} koster {num1} kroner. Hvor mange kan {name} kjøpe for {num2} kroner?"
        ],
        'items': ['epler', 'bøker', 'blyanter', 'is', 'boller', 'godteri']
    },
    'sharing': {
        'templates': [
            "{name} har {num1} {item} og vil dele likt med {num2} venner. Hvor mange {item} får hver person?",
            "Det er {num1} {item} som skal deles likt mellom {num2} barn. Hvor mange {item} får hvert barn?"
        ],
        'items': ['kjeks', 'ballonger', 'klistremerker', 'drops', 'baller']
    },
    'time': {
        'templates': [
            "Bussen bruker {num1} minutter fra {place1} til {place2}. Hvis bussen starter klokken {time}, når kommer den fram?",
            "{name} begynner på skolen klokken {time} og er der i {num1} timer. Når slutter {name} på skolen?"
        ],
        'places': ['skolen', 'butikken', 'parken', 'biblioteket', 'svømmehallen']
    },
    'measurement': {
        'templates': [
            "Et gjerde er {num1} meter langt. Hvis hver planke er {num2} meter bred, hvor mange planker trengs?",
            "En hage er {num1} meter lang og {num2} meter bred. Hva er arealet av hagen?",
            "{name} har et tau som er {num1} meter langt. {name} klipper det i biter på {num2} meter. Hvor mange biter får {name}?"
        ]
    }
}

# 添加挪威语名字列表
_norwegian_names = [
    'Ole', 'Lars', 'Erik', 'Anders', 'Per',
    'Anna', 'Maria', 'Ingrid', 'Emma', 'Sofia'
]

async def generate_word_problem(age: int) -> dict:
    """生成应用题"""
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
        if num2 == 0:  # 避免除以零
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
    
    # 生成问题哈希值用于去重
    question_hash = hash(question)
    
    return {
        "question": question,
        "answer": float(answer),
        "type": "word_problem",
        "sub_type": problem_type,
        "hash": question_hash,
        "difficulty": get_difficulty_by_age(age),
        "age": age
    }