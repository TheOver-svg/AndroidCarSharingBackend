import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.secutiry import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="Недійсний токен")
            
        return {"user_id": int(user_id)}
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Термін дії токена закінчився")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Недійсний токен")