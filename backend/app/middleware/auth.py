from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from ..core.config import settings

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Kunne ikke validere legitimasjon"
        )

class AuthMiddleware:
    async def __call__(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)
            
        public_paths = [
            '/api/auth/login',
            '/api/auth/register'
        ]
            
        if any(request.url.path.endswith(path) for path in public_paths):
            return await call_next(request)
            
        try:
            auth = request.headers.get('Authorization')
            if not auth:
                raise HTTPException(
                    status_code=401,
                    detail="Mangler autorisasjon"
                )
                
            token = auth.split(' ')[1]
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=[settings.ALGORITHM]
            )
            request.state.user = payload
            
        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Ugyldig token"
            )
            
        return await call_next(request) 