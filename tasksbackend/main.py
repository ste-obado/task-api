#to do list
from database import Base, get_db,engine
from auth import password_hash,password_verify,access_token
from models import User,Task
from protection import protected_route
from schema import taskupdate, taskview,user,user_login
from fastapi import FastAPI, HTTPException,Depends
from sqlalchemy.orm import Session
from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm

Base.metadata.create_all(bind=engine)  # Create tables in the database
#create app
app =FastAPI()

#ROUTES-------------------------------------
@app.get("/")
def root():
   return {"message": "ready to roll!"}

#user registartion
@app.post("/register")
def register_user(new_user:user,db:Session = Depends(get_db)):
   #check if user exists
    existing_user=db.query(User).filter(User.email==new_user.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="User already exists")
    print("Password:", new_user.password)
    print("Length:", len(new_user.password))
    print("Type:", type(new_user.password))
    #create new user
    password=password_hash(new_user.password)
    db_new_user= User(username=new_user.username,email=new_user.email,password=password)
  
    db.add(db_new_user)
    db.commit()
    db.refresh(db_new_user)
    return db_new_user

#user_login
#@app.post("/login")
#def login_user(user:user_login,db:Session = Depends(get_db)):


@app.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=400,
            detail="Invalid email or password"
        )

    if not password_verify(form_data.password, existing_user.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid email or password"
        )

    token_data = {"sub": str(existing_user.id)}
    token = access_token(token_data)

    return {
        "access_token": token,
        "token_type": "bearer"
    }


    #check if user exists
    #existing_user=db.query(User).filter(User.email==user.email).first()
    #if not existing_user:
        #raise HTTPException(status_code=400,detail="Invalid email or password")

    #verify password to match the existing user password
    #if not password_verify(user.password,existing_user.password):
        #raise HTTPException(status_code=400,detail="Invalid email or password")

    #create access token
    #token_data={"sub":existing_user.id}
    #token=access_token(token_data)
    #return {"access_token":token,"token_type":"bearer"}


###------------------PROTECTED ROUTES-----------------------------

#get all tasks
@app.get("/all_tasks")
def get_tasks(db:Session = Depends(get_db),current_user:User = Depends(protected_route)):
   tasks=db.query(Task).all()
   return tasks

#get chosen  tasks
@app.get("/tasks/count")
def count_tasks(user:User = Depends(protected_route),db:Session = Depends(get_db), skip: Optional[int] = 0, limit: Optional[int] = 0):
    tasks = db.query(Task).filter(Task.user_id == user.id).offset(skip).limit(limit).all()
    if limit is None:
        return {"count": len(tasks[skip:])}
    return {"count": len(tasks[skip:skip + limit])}

#filter tasks by status
@app.get("/tasks/filter")
def filter_task(user:User = Depends(protected_route),status:Optional[str]=None,db:Session = Depends(get_db)):
      filtered_tasks=db.query(Task).filter(Task.status == status,Task.user_id == user.id).all()
    
      if not filtered_tasks:
        return {"message": "No tasks found with the specified filters"}
      return filtered_tasks
   
   
@app.get("/tasks/sort")
def sort_tasks(user:User = Depends(protected_route),db:Session = Depends(get_db),sort_by:Optional[str]=None):
   tasks=db.query(Task).filter(Task.user_id == user.id).all()
   if sort_by=="due_date":
      sorted_tasks=sorted(tasks, key=lambda x: x.due_date)
     
   
   elif sort_by=="status":
      status_order={"pending":1,"inprogress":2,"completed":3}
      sorted_tasks=sorted(tasks, key=lambda x: status_order.get(x.status, 0))
      

   else:
      return {"message":"Invalid sort_by value. Use 'due_date' or 'status'."}
   return sorted_tasks

#@app.get("/tasks/summary")
#def get_tasks_summary():
 #   total_tasks = len(tasks)
  #  completed_tasks = len([task for task in tasks if task["status"] == "completed"])
   # pending_tasks = len([task for task in tasks if task["status"] == "pending"])
    #in_progress_tasks = len([task for task in tasks if task["status"] == "inprogress"])
    
    #return {
     #   "total_tasks": total_tasks,
      #  "completed_tasks": completed_tasks,
       # "pending_tasks": pending_tasks,
        #"in_progress_tasks": in_progress_tasks
    #}

@app.get("/tasks/summary")
def get_tasks_summary(user:User = Depends(protected_route),db:Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.user_id == user.id).all()
    summary = {
        "total_tasks": len(tasks),
        "completed_tasks": 0,
        "pending_tasks": 0,
        "in_progress_tasks": 0
    }

    for task in tasks:
        status = task.status.lower()
        if status == "completed":
            summary["completed_tasks"] += 1
        elif status == "pending":
            summary["pending_tasks"] += 1
        elif status in ["inprogress", "in_progress"]:
            summary["in_progress_tasks"] += 1

    return summary


#get one task
@app.get("/tasks/{task_id}")
def get_task(task_id:int,user:User = Depends(protected_route),db:Session = Depends(get_db)):
   task=db.query(Task).filter(Task.id==task_id,Task.user_id==user.id).first()
   if not task:
       raise HTTPException(status_code=404,detail="Task not found")
   return task

#add tasks
@app.post("/add_tasks")
def add_task(new_task:taskview,user:User = Depends(protected_route),db:Session = Depends(get_db)):
  #new_task.user_id = user.id
  db_newtask =Task(title=new_task.title,status=new_task.status,due_date=new_task.due_date,user_id=user.id)
  db.add(db_newtask)
  db.commit()
  db.refresh(db_newtask)
  return{"message":"Task added","TASK":db_newtask}


   

#mark task as completed

@app.post("/tasks/{task_id}/completed")
def mark_task_completed(task_id:int,user:User = Depends(protected_route),db:Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    #task.update({"status": "completed"})
    task.status = "completed"
    db.commit()
    db.refresh(task)
    return {"message":"Task marked as completed","TASK":task}



   

#update one task
@app.patch("/update_task/{task_id}")
def update_task_status(task_id:int,taskupdate,user:User = Depends(protected_route),db:Session = Depends(get_db)):
   task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
   if not task:
        raise HTTPException(status_code=404,detail="Task not found")
  
   db.commit()
   db.refresh(task)       
   return {"message":"Task updated","TASK":task}    
     
  


#delete
@app.delete("/tasks/{task_id}")
def delete_task(task_id:int,user:User = Depends(protected_route),db:Session = Depends(get_db)):
   task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
   if not task:
        raise HTTPException(status_code=404,detail="Task not found")
   db.delete(task)
   db.commit()
   return {"message":"Task deleted"}  


