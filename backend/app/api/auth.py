from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from ..models.user import User, UserType
from ..core.database import get_db
from ..core.logger import logger
from pydantic import BaseModel
from typing import Optional
from ..core.config import settings

router = APIRouter()

# 密码加密配置
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,
    bcrypt__ident="2b"
)

# OAuth2 配置
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# 添加请求模型
class UserRegister(BaseModel):
    username: str
    password: str
    email: str
    role: UserType
    age: Optional[int] = None

# 用户注册
@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    try:
        logger.debug(f"Registration attempt for user: {user_data.username}")
        
        # 检查用户名是否已存在
        if db.query(User).filter(User.username == user_data.username).first():
            logger.error(f"Username already exists: {user_data.username}")
            raise HTTPException(
                status_code=400,
                detail="Brukernavnet er allerede i bruk"
            )
            
        # 检查邮箱是否已存在
        if db.query(User).filter(User.email == user_data.email).first():
            logger.error(f"Email already exists: {user_data.email}")
            raise HTTPException(
                status_code=400,
                detail="E-postadressen er allerede i bruk"
            )
            
        # 创建新用户
        hashed_password = pwd_context.hash(user_data.password)
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            role=user_data.role,
            age=user_data.age
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.debug(f"Registration successful for user: {user_data.username}")
        return {"message": "Registrering vellykket"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=500,
            detail="En feil oppstod under registrering"
        )

# 用户登录
@router.post("/auth/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    try:
        logger.debug(f"Login attempt for user: {form_data.username}")
        
        # 查找用户
        user = db.query(User).filter(User.username == form_data.username).first()
        if not user:
            logger.error(f"User not found: {form_data.username}")
            raise HTTPException(
                status_code=401,
                detail="Feil brukernavn eller passord",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # 验证密码
        if not pwd_context.verify(form_data.password, user.hashed_password):
            logger.error(f"Invalid password for user: {form_data.username}")
            raise HTTPException(
                status_code=401,
                detail="Feil brukernavn eller passord",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # 生成访问令牌
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "role": user.role.value},
            expires_delta=access_token_expires
        )
        
        logger.debug(f"Login successful for user: {form_data.username}")
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role.value,
                "age": user.age
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=500,
            detail="En feil oppstod under pålogging"
        )

# 创建访问令牌
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # 默认24小时过期
        expire = datetime.utcnow() + timedelta(minutes=1440)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

# 获取当前用户
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Kunne ikke validere legitimasjon",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        logger.error(f"Token validation error: {e}")
        raise credentials_exception
        
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        logger.error(f"User not found: {username}")
        raise credentials_exception
        
    return user 