from .. import models, schemas
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()

@router.get("/posts", response_model=list[schemas.Post])
def get_posts(db:Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts")
    # posts = dict_cursor(cursor)
    posts = db.query(models.Post).all()
    return posts

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db:Session = Depends(get_db)):
    # cursor.execute("INSERT INTO posts (title, content, published) OUTPUT INSERTED.* VALUES (?, ?, ?)",
    #                post.title, post.content, post.published)
    # new_post = dict_cursor(cursor)
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db:Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts WHERE id = ?", id)
    # post = dict_cursor(cursor)
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db)):
    # cursor.execute("DELETE FROM posts WHERE id = ?", id)
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=404, detail="Post id: {id} not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db:Session = Depends(get_db)):
    # cursor.execute("UPDATE posts SET title = ?, content = ?, published = ? WHERE id = ?",
    #                 post.title, post.content, post.published, id)

    # conn.commit()
    # cursor.execute("SELECT * FROM posts WHERE id = ?", id)
    # updated_post = dict_cursor(cursor)

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=404, detail= f"Post {id} not found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()