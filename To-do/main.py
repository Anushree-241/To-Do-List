import sqlite3
from fastapi import FastAPI, Query, Request, Cookie
from fastapi.params import Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import starlette.status as status 
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials

DATABASE_NAME = "todo.db"
todo = FastAPI()
security = HTTPBasic()
todo.mount("/To-do/Static", StaticFiles(directory="Static"), name="Static")
templates = Jinja2Templates(directory="Template")
todo.add_middleware(SessionMiddleware, secret_key='todo')



@todo.get("/", response_class=HTMLResponse)
def task(request : Request):
    con = sqlite3.connect("todo.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from task where task_status = 0 ;" )
    tasks = cur.fetchall()
    cur.execute("select * from task where task_status = 1;" )
    tsk = cur.fetchall()
    con.close
    return templates.TemplateResponse("index.html", {"request" : request, "tasks" : tasks,"tsk":tsk})

@todo.post("/",response_class=HTMLResponse)
def post_todo(request :Request,task_desc:str =Form(...)):
    #database -> inserting or updating, can be done POST request
    # user_id = request.session.get('user_id')
    # if not request.session.get('isLogin'):
    #     return RedirectResponse('/lgn-usr', status_code=status.HTTP_302_FOUND)
    with sqlite3.connect("todo.db") as con:
        cur = con.cursor()
        cur.execute("INSERT into task(task_desc,task_status) values(?,?)",
                    (task_desc,0))
        con.commit()
        return templates.TemplateResponse("index.html",{"request": request ,"msg":"New Task added!"})
