from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Depends, Response, Request
from sqlalchemy.orm import Session
from ..database import SessionLocal, get_db
from ..schemas import UserCreate, UserResponse, UserLogin, Token
from ..models import User, RefreshToken
from ..utils.hashing import hash_password, verify_password
from ..oauth2 import create_token, create_refresh_token,get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post('/refreshtoken')
def new_access_token(request:Request, db:Session = Depends(get_db)):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="No refresh token provided")
    db_token = db.query(RefreshToken).filter(RefreshToken.token == token).first()
    if not db_token or db_token.revoked or db_token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_token = create_token({"user_id": db_token.user_id})
    return {"access_token": new_token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    data = db.query(User).filter(User.email == user.email).first()
    if data:
        raise HTTPException(status_code=400, detail="Email already registered")

    user.password = hash_password(user.password)
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post('/login', response_model=Token)
def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    currentuser = db.query(User).filter(User.email == user.email).first()
    if not currentuser or not verify_password(user.password, currentuser.password):
        raise HTTPException(status_code=400, detail="Invalid Credentials")

    access_token = create_token({"user_id": currentuser.id})
    token, expires = create_refresh_token()
    db_token = RefreshToken(token=token, user_id=currentuser.id, expires_at=expires)
    db.add(db_token)
    db.commit()
    response.set_cookie(key="refresh_token", value=token, httponly=True)


    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/logout')
def logout(request:Request, response: Response, db:Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    token = request.cookies.get("refresh_token")
    if token:
        db_token = db.query(RefreshToken).filter(RefreshToken.token == token).first()
        if db_token:
            db_token.revoked = True
            db.commit()
    response.delete_cookie(key="refresh_token")
    return {"message": "Successfully logged out"}