from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter;
from sqlalchemy.orm import Session;
from .. import schemas,models,OAuth2;
from ..database import get_db;
from typing import List,Optional
from sqlalchemy import func;

router = APIRouter( prefix = "/posts", tags=['posts'] )
@router.get("/",response_model=List[schemas.Post_Out])
def get_all_posts(db: Session = Depends(get_db),Limit:int = 10,skip:int =0,search:Optional[str]=""):
    
    # cursor.execute("""SELECT * FROM post""")
    # posts = cursor.fetchall();a
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all();
    posts = db.query(models.Post,func.count(models.Vote.post_id).label("Votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all();
    return posts


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: schemas.Create_Post,db: Session = Depends(get_db),current_user: int = Depends(OAuth2.get_current_user)):
#    cursor.execute("""INSERT INTO post (title,content,published) VALUES (%s,%s,%s) RETURNING *""", (post.title,post.content,post.published)  );
#    new_post = cursor.fetchone();
#    conn.commit();
    new_post = models.Post( owner_id = current_user.id,**post.model_dump()  );
    db.add(new_post);
    db.commit();
    db.refresh(new_post);
    return new_post

@router.get("/{id}",response_model=schemas.Post_Out)
def get_post(id:int,response: Response,db: Session = Depends(get_db),current_user: int = Depends(OAuth2.get_current_user)):
#  cursor.execute("""SELECT * FROM post WHERE id=%s """,(str(id),));
#  post = cursor.fetchone();
#  post = db.query(models.Post).filter(models.Post.id == id).first();
 
 post = db.query(models.Post,func.count(models.Vote.post_id).label("Votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first();
 
 
 if not post:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist");
 
 return post;

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user: int = Depends(OAuth2.get_current_user)):
    # cursor.execute(""" DELETE FROM post WHERE id=%s RETURNING *""",(str(id),));
    # has_del = cursor.fetchone();
    post_query = db.query(models.Post).filter(models.Post.id == id);
    post = post_query.first();
    
    if not post: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist");
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action");
    
    post_query.delete(synchronize_session=False);
    
    db.commit();

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED,response_model=schemas.Post)
def update_post(id:int,updated_post:schemas.Create_Post,db: Session = Depends(get_db),current_user: int = Depends(OAuth2.get_current_user)):
#   cursor.execute(""" UPDATE post SET title=%s, content=%s, published=%s WHERE id=%s RETURNING* """,(post.title,post.content,post.published,str(id),))
#   updated_post = cursor.fetchone();
  post_query = db.query(models.Post).filter(models.Post.id == id);
  post = post_query.first();
  
  if post is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist");
  
  if post.owner_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action");
  
  post_query.update(updated_post.model_dump(), synchronize_session=False)
  db.commit();
  return post_query.first();
