from fastapi import APIRouter,Depends
from app.models.todo import CreateTodo
from app.database.schema.todo_schema import Todo
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database.db import get_db
from app.dependencies import authenticte_user

router=APIRouter(prefix="/todos",tags=["Todos"],dependencies=[Depends(authenticte_user)])


@router.get("/")
def index(db: Annotated[Session, Depends(get_db)]):
    stmt=select(Todo.id,Todo.content,Todo.is_completed)
    todos=db.execute(stmt).mappings().all()
    return {"messages":"this is todo router","data":todos}


@router.get("/{id}")
def get_todo(id:int,db: Annotated[Session, Depends(get_db)]):
    stmt=select(Todo.id,Todo.content,Todo.is_completed).where(Todo.id==id)
    todo=db.execute(stmt).mappings().first()
    return {"messages":"this is todo router","data":todo}

@router.post("/")
def create_todo(item:CreateTodo, db: Annotated[Session, Depends(get_db)]):
    db_todo = Todo(content=item.content,is_completed=item.is_completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return {"messages":"created a todo item","data":db_todo.model_dump()}

@router.delete("/{id}")
def delete_todo(id:int, db: Annotated[Session, Depends(get_db)]):
    stmt=select(Todo).where(Todo.id==id)
    todo=db.execute(stmt).scalar_one_or_none()
    if not todo:
        return {"messages":"todo item not found"}
    db.delete(todo)
    db.commit()
    return {"messages":"deleted a todo item","data":todo.model_dump()}