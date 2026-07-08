
from pydantic import BaseModel,field_validator,EmailStr,model_validator
from typing import Optional
from datetime import datetime

#user schema
class user(BaseModel):
    username :str
    email :EmailStr
    password :str
    confirm_password :str

    @field_validator("password")
    def validate_password(cls,password):
        if len(password)<6:
            raise ValueError("Password must be at least 6 characters long")
        return password
    
    @model_validator(mode="after")
    def password_verify(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
    
  
#user login schema    
class user_login(BaseModel):
    email:EmailStr
    password:str


#task schema
class taskview(BaseModel):
    title :str
    status:str = "pending"
    due_date:  datetime

    #validate status
    @field_validator("status")
    def validate_status(cls,status):
        if status not in ["pending","inprogress","completed"]:
            raise ValueError("Status must be pending, inprogress, or completed")
        return status
    

    #validate due_date
    @field_validator("due_date")
    def validate_due_date(cls,date):
        try:
         datetime.strftime(date,"%Y-%m-%d ")
        except:
            raise ValueError("Due date must be in YYYY-MM-DD format")
        return date

    #validate due_date is in future
    @field_validator("due_date")
    def validate_due_date_in_future(cls,due_date):
        if due_date < datetime.now():
            raise ValueError("Due date must be in future")
        return due_date
    

class taskupdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None

    class Config:
          from_attributes = True 
         
    




