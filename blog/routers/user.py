from fastapi import Depends, FastAPI, Response, status,HTTPException
from blog import hasghing, models, schemas
from blog.database import SessionLocal, get_db
from typing import List
from sqlalchemy.orm import Session

from fastapi import APIRouter

router=APIRouter(tags=['User'],
                 prefix="/user")


@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.ShowUser)
def create_user(request:schemas.User,db:Session=Depends(get_db)):
    new_user=models.UserModel(name=request.name,email=request.email,password=hasghing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.get('/{id}/',response_model=schemas.ShowUser)
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.UserModel).filter(models.UserModel.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with the id {id} not found ")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail':f"Blog with the id {id} not found "}
    return user
