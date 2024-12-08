from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Table, ARRAY
from sqlalchemy.orm import relationship
from .user import Base, MathKnowledgePoints
from ..core.logger import logger

# 年龄-知识点映射表
class AgeKnowledgeMapping(Base):
    __tablename__ = "age_knowledge_mappings"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer, nullable=False)
    knowledge_point = Column(String, nullable=False)  # 存储知识点的枚举值

# 知识点-题目类型映射表
class KnowledgeTypesMapping(Base):
    __tablename__ = "knowledge_types_mappings"

    id = Column(Integer, primary_key=True, index=True)
    knowledge_point = Column(String, nullable=False)  # 知识点代码
    problem_types = Column(String, nullable=False)  # 题目类型，用逗号分隔

# 年龄-题目类型映射表
class AgeTypesMapping(Base):
    __tablename__ = "age_types_mappings"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer, nullable=False)
    problem_types = Column(String, nullable=False)  # 题目类型，用逗号分隔

def init_problem_types_mappings(db_session):
    """初始化题目类型映射数据"""
    try:
        # 检查知识点映射是否已存在
        existing_knowledge_count = db_session.query(KnowledgeTypesMapping).count()
        if existing_knowledge_count == 0:
            # 知识点题目类型映射
            knowledge_mappings = [
                {
                    "knowledge_point": MathKnowledgePoints.ADDITION_BASIC.value,
                    "problem_types": "basic,shopping"
                },
                {
                    "knowledge_point": MathKnowledgePoints.SUBTRACTION_BASIC.value,
                    "problem_types": "basic,shopping"
                },
                {
                    "knowledge_point": MathKnowledgePoints.MULTIPLICATION_BASIC.value,
                    "problem_types": "basic,sharing"
                },
                {
                    "knowledge_point": MathKnowledgePoints.DIVISION_BASIC.value,
                    "problem_types": "basic,sharing"
                },
                {
                    "knowledge_point": MathKnowledgePoints.FRACTION_CONCEPT.value,
                    "problem_types": "basic,sharing"
                },
                {
                    "knowledge_point": MathKnowledgePoints.DECIMAL_CONCEPT.value,
                    "problem_types": "basic,measurement"
                },
                {
                    "knowledge_point": MathKnowledgePoints.SHAPES_2D.value,
                    "problem_types": "measurement"
                },
                {
                    "knowledge_point": MathKnowledgePoints.PERIMETER.value,
                    "problem_types": "measurement"
                },
                {
                    "knowledge_point": MathKnowledgePoints.AREA.value,
                    "problem_types": "measurement"
                },
                {
                    "knowledge_point": MathKnowledgePoints.SIMPLE_EQUATIONS.value,
                    "problem_types": "basic"
                },
                {
                    "knowledge_point": MathKnowledgePoints.VARIABLES.value,
                    "problem_types": "basic"
                },
                {
                    "knowledge_point": MathKnowledgePoints.NUMBER_SEQUENCE.value,
                    "problem_types": "basic"
                },
                {
                    "knowledge_point": MathKnowledgePoints.PLACE_VALUE.value,
                    "problem_types": "basic"
                }
            ]
            
            for mapping in knowledge_mappings:
                db_session.add(KnowledgeTypesMapping(**mapping))
            
            logger.info(f"Initialized {len(knowledge_mappings)} knowledge type mappings")

        # 检查年龄映射是否已存在
        existing_age_count = db_session.query(AgeTypesMapping).count()
        if existing_age_count == 0:
            # 年龄题目类型映射
            age_mappings = [
                {
                    "age": 6,
                    "problem_types": "basic,shopping"
                },
                {
                    "age": 7,
                    "problem_types": "basic,shopping"
                },
                {
                    "age": 8,
                    "problem_types": "basic,shopping,sharing"
                },
                {
                    "age": 9,
                    "problem_types": "basic,shopping,sharing"
                },
                {
                    "age": 10,
                    "problem_types": "basic,shopping,sharing,measurement"
                },
                {
                    "age": 11,
                    "problem_types": "basic,shopping,sharing,measurement,time"
                },
                {
                    "age": 12,
                    "problem_types": "basic,shopping,sharing,measurement,time"
                }
            ]
            
            for mapping in age_mappings:
                db_session.add(AgeTypesMapping(**mapping))
            
            logger.info(f"Initialized {len(age_mappings)} age type mappings")

        db_session.commit()
        
    except Exception as e:
        db_session.rollback()
        logger.error(f"Error initializing problem types mappings: {e}")
        raise 

   