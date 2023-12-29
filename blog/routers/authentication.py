from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from blog import models, schemas
from sqlalchemy.orm import Session
from blog import database
from blog.database import SessionLocal, get_db
from blog.hasghing import Hash
from blog.token import create_access_token




router=APIRouter(tags=['Authentication'])


@router.post('/login/')
def login_user(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    user=db.query(models.UserModel).filter(models.UserModel.email==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials ")
    if not Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Wrong password ")

    access_token = create_access_token(data={"sub": user.email})
    return access_token
