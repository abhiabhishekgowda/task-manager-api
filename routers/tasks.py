from fastapi import APIRouter,HTTPException,status,Query,Depends
from database import TaskDatabase,get_db
from schemas import TaskCreate,TaskResponse,TaskUpdate

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.post("",response_model=TaskResponse,status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate,db: TaskDatabase = Depends(get_db)):
    return db.create_task(task.title,task.completed)

@router.get("",response_model=list[TaskResponse],)
def get_all_task(completed: bool | None = None,search: str | None = None, limit: int=Query(default=10,ge=1,le=100),skip: int = Query(default=0,ge=0),db: TaskDatabse = Depends(get_db)):
    return db.get_all_tasks(completed=completed,search=search,limit=limit,skip=skip)

@router.get("/{task_id}",response_model=TaskResponse)
def get_task(task_id: int,db: TaskDatabase = Depends(get_db)):
    task = db.get_task(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task Not Found")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskUpdate,db: TaskDatabase = Depends(TaskDatabase)):
    updated_task = db.update_task(
        task_id=task_id, 
        title=task_data.title, 
        completed=task_data.completed
    )
    if not updated_task:
       raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Task not found"
        )
    return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int,db: TaskDatabase = Depends(get_db)):
    deleted = db.delete_task(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Task not found"
        )
    return {"message": "Task deleted successfully"}

