from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter;
from sqlalchemy.orm import Session;
from .. import schemas,models,util,OAuth2;
from ..database import get_db;
from typing import List;
  
  
router = APIRouter( prefix = "/users", tags=['users'] );
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.User_Out)
def create_user(user:schemas.User_Create, db: Session = Depends(get_db)):
    hash_password = util.hash(user.password);
    user.password = hash_password;
    created_user = models.User( **user.model_dump() );
    db.add(created_user);
    db.commit();
    db.refresh(created_user);
    if not created_user: raise HTTPException(status_code=status.HTTP_500_NOT_FOUND, detail="Something went wrong whilst creating the user ");
    return created_user;

@router.get("/{id}", response_model=schemas.User_Out)
def get_user(id:int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first();
    if not user: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist");
    return user;
    
@router.get("/",status_code=status.HTTP_200_OK,response_model=List[schemas.User_Out])
def get_all_user(db:Session = Depends(get_db),current_user: int = Depends(OAuth2.get_current_user)):
    users = db.query(models.User).all();
    return users;