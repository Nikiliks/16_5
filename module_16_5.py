from fastapi import FastAPI, status, Body, HTTPException, Path, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Annotated, List
from fastapi.templating import Jinja2Templates



app = FastAPI()
templates = Jinja2Templates(directory="templates")
users = []


class User(BaseModel):
    id: int
    username: str
    age: int

@app.get("/")
async def req(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users_list": users})

@app.get("/user/{user_id}")
async def get_users(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id]})
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')

@app.post("/user/{username}/{age}")
async def append_user(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', examples='Example')],
                    age: Annotated[int, Path(le=120, ge=18, description='Enter age', examples='18')])-> User:
    user_id = (users[-1].id + 1) if users else 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put("/user/{user_id}/{username}/{age}")
async def update_users(user_id: Annotated[int, Path(gt=0, lt=100, description='Enter User ID', examples='1')],
                      username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', examples='Example')],
                    age: Annotated[int, Path(le=120, ge=18, description='Enter age', examples='18')]) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    else:
        raise HTTPException(status_code=404, detail='User was not found')

@app.delete( '/user/{user_id}')
async def delete_users(
        user_id: Annotated[int, Path(ge=1, le=100, description='Enter user id', examples='1')]) -> str:
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")



#Запуск: uvicorn module_16_5:app --reload
