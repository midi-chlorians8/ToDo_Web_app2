from dotenv import load_dotenv
# from pathlib import Path
import os
# dotenv_path = Path('.env')
load_dotenv()


# DataBase
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL') #"postgresql://postgres:postgres@localhost/postgres" #os.getenv('SQLALCHEMY_DATABASE_URI') #"postgresql://postgres:postgres@localhost/postgres"
print(type(os.getenv('SQLALCHEMY_DATABASE_URL')))
print(type("postgresql://user:password@postgresserver/db"))
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass
# DataBase


# Models
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from pydantic import BaseModel


class Note(Base):
    __tablename__ = "notes"
     
    id = Column(Integer, primary_key=True, index=True) # id заметки. Незнаю пока наскок нада эта колонка
    name = Column(String, unique=True, index=True)
    description = Column(String)
    users_id = Column(Integer) #Какому юзеру принадлежит заметка
# Models

Base.metadata.create_all(bind=engine)

db = SessionLocal()



#Cервер
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import uvicorn

app = FastAPI()


class Note_Pydant(BaseModel):
    id: int
    name: str
    description: str | None = None


# notedict = {
#   "name": "Holo",
#   "description": "avc"
# }


@app.post("/send_note/")
def create_item(item: Note_Pydant): # Вот так вот ловим body http post запроса
    notedict = item.dict()
    db_note = Note(name = notedict.get("name"), description = notedict.get("description"))

    # # Узнать сколько у нас записей в таблице
    # count = 0
    # with engine.connect() as connection:
    #     result = connection.execute(text("select count(id) from notes"))
    #     for row in result:
    #         count = row.count +1 #  Чтоб заработало и найти совпадающее имя при запросе на добавление записи в бд.
    #         #print(row.count)
    #         print(f"row count: {count}")
    #         #pass
    # # Узнать сколько у нас записей в таблице buy ring go to shop2

    # #Сравниваем db_note которую хотим добавить в код и получаем список записей из базы данных.
    # for i in range(1,count):
    #     print(i)
    #     print(f"Received command: {i}")
    #     res = db.get(Note, i)
    #     print(res.name)
    #     print(db_note.name)
    #     if res.name == db_note.name:
    #         print("ERROR")
    #         raise HTTPException(status_code=404, detail="I can not add row with the same name")
    # #Сравниваем db_note которую хотим добавить в код и получаем список записей из базы данных.
    
    note_exists = db.query(exists().where(Note.name == db_note.name)).scalar() #использовать запрос, чтобы проверить, существует ли заметка с таким же именем
    if note_exists:
        raise HTTPException(status_code=404, detail="Cannot add row with the same name")
    
    db.add(db_note)
    db.commit()
    return item

@app.get("/get_note/")
def read_item(skip: int = 0, limit: int = 10):
    return db.query(Note).offset(skip).limit(limit).all()


@app.delete("/del_note/{note_id}")
def delete_note(note_id: int):
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()    
    return {"ok": True}





# Вывод страницы с заметками 
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/notes_html/{user_id}", response_class=HTMLResponse) # user_id для будущего апгрейда для мультиюзеров
async def read_item(request: Request, user_id: str, skip: int = 0, limit: int = 10):
    read_notes = db.query(Note).offset(skip).limit(limit).all()
    return templates.TemplateResponse("item.html", {"request": request, "id": read_notes})

class Command(BaseModel):
    command: str

@app.post("/process_command")
async def process_command(command: Command):
    # replace this with the actual code to process the command
    print(f"Received command: {command.command}")
    return {"status": "Command received and processed successfully"}
# Вывод страницы с заметками 


# Тестируем вывод новой страницы с заметками
#from fastapi import FastAPI
#from pydantic import BaseModel

#app = FastAPI()

class Task(BaseModel):
    name: str
    description: str

@app.get("/notes2_html/{user_id}", response_class=HTMLResponse) # user_id для будущего апгрейда для мультиюзеров
async def read_item(request: Request, user_id: str, skip: int = 0, limit: int = 10):
    read_notes = db.query(Note).offset(skip).limit(limit).all()
    return templates.TemplateResponse("test4_gpt.html", {"request": request, "id": read_notes})


from sqlalchemy import exists
@app.post("/tasks") # Принять от кнопки создать body
def create_task(task: Task):
    task_dict = task.dict()
    # Do something with the task data, such as saving it to a database
    notedict = task_dict
    db_note = Note(name = notedict.get("name"), description = notedict.get("description"))

    note_exists = db.query(exists().where(Note.name == db_note.name)).scalar() #использовать запрос, чтобы проверить, существует ли заметка с таким же именем
    if note_exists:
        raise HTTPException(status_code=404, detail="Cannot add row with the same name")
    # # Узнать сколько у нас записей в таблице
    # count = 0
    # with engine.connect() as connection:
    #     result = connection.execute(text("select count(id) from notes"))
    #     for row in result:
    #         count = row.count +1 #  Чтоб заработало и найти совпадающее имя при запросе на добавление записи в бд.
    #         #print(row.count)
    #         print(f"row count: {count}")
    #         #pass
    # # Узнать сколько у нас записей в таблице buy ring go to shop2

    # #Сравниваем db_note которую хотим добавить в код и получаем список записей из базы данных.
    # for i in range(1,count):
    #     #print(i)
    #     print(f"Received command: {i}")
    #     res = db.get(Note, i)
    #     print(res.name)
    #     print(db_note.name)
    #     if res.name == db_note.name:
    #         print("ERROR")
    #         raise HTTPException(status_code=404, detail="I can not add row with the same name")
    # #Сравниваем db_note которую хотим добавить в код и получаем список записей из базы данных.
    
    db.add(db_note)
    db.commit()
    return {"message": "Task created successfully"}
# Тестируем вывод новой страницы с заметками

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # run app on the host and port
   


