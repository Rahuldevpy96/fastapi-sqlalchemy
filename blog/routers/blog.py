from fastapi import Depends, FastAPI, Response, status,HTTPException
from blog import models, schemas
from blog.database import SessionLocal, get_db
from typing import List
from sqlalchemy.orm import Session

from fastapi import APIRouter

from blog.oauth2 import get_current_user

router=APIRouter(tags=['Blog'],
                 prefix="/blog"
                 )

@router.get('/',response_model=List[schemas.ShowBlog])
def all(db:SessionLocal=Depends(get_db),get_current_user:schemas.User=Depends(get_current_user)):
    blogs=db.query(models.BlogModel).all()
    return blogs



@router.post('/',status_code=status.HTTP_201_CREATED)
def blog(request:schemas.Blog,db:Session=Depends(get_db),get_current_user:schemas.User=Depends(get_current_user)):
    new_blog=models.BlogModel(title=request.title, body=request.body,users_id=4)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get('/{id}',status_code=200,response_model=schemas.ShowBlog)
def  get(id,response:Response,db:Session=Depends(get_db),get_current_user:schemas.User=Depends(get_current_user)):
    blog=db.query(models.BlogModel).filter(models.BlogModel.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} not found ")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail':f"Blog with the id {id} not found "}
    return blog


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id,db:Session=Depends(get_db),get_current_user:schemas.User=Depends(get_current_user)):
    blog=db.query(models.BlogModel).filter(models.BlogModel.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id{id} not found")
    else:
        blog.delete(synchronize_session=False)

    db.commit()
    return 'Done'

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,request:schemas.Blog,db:Session=Depends(get_db),get_current_user:schemas.User=Depends(get_current_user)):
    blog=db.query(models.BlogModel).filter(models.BlogModel.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id{id} not found")
    else:
        blog.update({"title":request.title,'body':request.body})

    db.commit()
    return 'Updated'
