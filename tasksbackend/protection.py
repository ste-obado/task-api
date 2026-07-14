
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from auth import token_verification
from database import get_db
from sqlalchemy.orm import Session
from models import User



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def protected_route(token: str = Depends(oauth2_scheme),db:Session = Depends(get_db)):
    credential_Error =HTTPException(
        status_code=401,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    #verify the token 
    payload =token_verification(token)
    if not payload:
        raise credential_Error
   
    #isolate user_id from the payload
    user_id = payload.get("sub")

    #verify the user_id is present
    if user_id is None:
        raise credential_Error
    
    #get the username from the database
    user=db.query(User).filter(User.id == user_id).first()

    if not user:
        raise credential_Error
    return user
