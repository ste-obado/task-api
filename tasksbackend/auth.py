from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException
from tasksbackend.config import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES



pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

def password_hash(password: str)->str:
    return pwd_context.hash(password)

def password_verify(password:str,hashed_password:str)->bool:
    return pwd_context.verify(password,hashed_password)

#token verfivation and access
def access_token(data:dict)->str:
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token
#verification
def token_verification(token:str)->dict:
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")