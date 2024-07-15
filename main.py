import uvicorn

from fastapi import FastAPI, Body, Depends
from app.model import *
from app.auth.handler import signJWT
from app.auth.bearer import Bearer

posts = [
    {
        "id": 1,
        "title": "I love Penguins ",
        "text": "Penguins are silly animals",
    }
]

app = FastAPI()

users = []

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

# testing
@app.get("/")
def greet():
    return {"hello": "world!."}

@app.get("/posts", tags=["posts"])
def get_posts():
    return posts

@app.post("/posts", dependencies=[Depends(Bearer())],tags=["posts"])
def create_post(post: PostSchema = Body(...)):
    posts.append(post)
    return post

@app.post("/user/signup", tags=["user"])
def create_user(user: UserSchema = Body(...)):
    users.append(user) # replace with db call, making sure to hash the password first
    return signJWT(user.email)

@app.get("/users", tags=["users"])
def get_users():
    return users

@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }