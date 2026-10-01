import fastapi
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello!" : "Welcome to this Greeting Application!!!"}

@app.get("/Greet/{Name}")
def read_item(Name: str, Val: str = "Have a Great Day Ahead!"):
    return {"Name": Name, "Greeting": Val}