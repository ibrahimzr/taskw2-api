from fastapi import APIRouter,Depends,status,Query,HTTPException
from sqlmodel import Session,select
from app.database import get_session
from app.models import Account,TaskItem
from app.dtos.requests import NewTask,TaskEdit
from app.dtos.responses import TaskView
from app.dependencies import get_current_user
from app.enums import Role,Status,Priority

task_router=APIRouter(prefix="/tasks",tags=["Tasks"])

def get_task_item(task_id:int,session:Session,account:Account):
    task_item=session.get(TaskItem,task_id)
    if not task_item:
        raise HTTPException(status_code=404,detail="Task not found")
    if account.role!=Role.admin and task_item.user_id!=account.id:
        raise HTTPException(status_code=404,detail="Task not found")
    return task_item

@task_router.post("",response_model=TaskView,status_code=status.HTTP_201_CREATED)
def create_task(data:NewTask,session:Session=Depends(get_session),account:Account=Depends(get_current_user)):
    task_item=TaskItem(title=data.title,description=data.description,priority=data.priority,due_date=data.due_date,user_id=account.id)
    session.add(task_item)
    session.commit()
    session.refresh(task_item)
    return task_item

@task_router.get("",response_model=list[TaskView])
def get_tasks(status_filter:Status|None=None,priority_filter:Priority|None=None,skip:int=Query(default=0,ge=0),limit:int=Query(default=30,ge=1,le=120),session:Session=Depends(get_session),account:Account=Depends(get_current_user)):
    statement=select(TaskItem)
    if account.role!=Role.admin:
        statement=statement.where(TaskItem.user_id==account.id)
    if status_filter:
        statement=statement.where(TaskItem.status==status_filter)
    if priority_filter:
        statement=statement.where(TaskItem.priority==priority_filter)
    statement=statement.order_by(TaskItem.id.desc()).offset(skip).limit(limit)
    return session.exec(statement).all()

@task_router.get("/{task_id}",response_model=TaskView)
def get_task(task_id:int,session:Session=Depends(get_session),account:Account=Depends(get_current_user)):
    return get_task_item(task_id,session,account)

@task_router.patch("/{task_id}",response_model=TaskView)
def update_task(task_id:int,data:TaskEdit,session:Session=Depends(get_session),account:Account=Depends(get_current_user)):
    task_item=get_task_item(task_id,session,account)
    changes=data.model_dump(exclude_unset=True)
    for key,value in changes.items():
        setattr(task_item,key,value)
    session.add(task_item)
    session.commit()
    session.refresh(task_item)
    return task_item

@task_router.patch("/{task_id}/complete",response_model=TaskView)
def complete_task(task_id:int,session:Session=Depends(get_session),account:Account=Depends(get_current_user)):
    task_item=get_task_item(task_id,session,account)
    if task_item.status==Status.done:
        raise HTTPException(status_code=400,detail="Task is already completed")
    task_item.status=Status.done
    session.add(task_item)
    session.commit()
    session.refresh(task_item)
    return task_item

@task_router.delete("/{task_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id:int,session:Session=Depends(get_session),account:Account=Depends(get_current_user)):
    task_item=get_task_item(task_id,session,account)
    session.delete(task_item)
    session.commit()