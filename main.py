from fastapi import FastAPI
from backend import get_films
app = FastAPI()

@app.post("/movie")
def input_films():
    get_films()