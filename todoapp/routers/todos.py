from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal, get_db
from ..models import User, Todo
from ..schemas import TodoCreate, TodoUpdate, TodoResponse
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)

# GET /todos → get all todos for logged in user
@router.get("/", response_model=list[TodoResponse])
def get_todos(skip: int = 0, limit: int = 10, search: str | None = None, completed: bool | None = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Todo).filter(Todo.user_id == current_user.id)
    if search is not None:
        query = query.filter(Todo.title.ilike(f"%{search}%"))

    if completed is not None:
        query = query.filter(Todo.completed == completed)
    return query.offset(skip).limit(limit).all()

# POST /todos → create a new todo
@router.post("/", response_model=TodoResponse, status_code=201)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_todo = Todo(title=todo.title, user_id=current_user.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

# PUT /todos/{id} → update a todo
@router.put("/{id}", response_model=TodoResponse)
def update_todo(id: int, todo: TodoUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_todo = db.query(Todo).filter(Todo.id == id, Todo.user_id == current_user.id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    if todo.title is not None:
        db_todo.title = todo.title
    if todo.completed is not None:
        db_todo.completed = todo.completed

    db.commit()
    db.refresh(db_todo)
    return db_todo

# DELETE /todos/{id} → delete a todo
@router.delete("/{id}")
def delete_todo(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_todo = db.query(Todo).filter(Todo.id == id, Todo.user_id == current_user.id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted successfully"}
