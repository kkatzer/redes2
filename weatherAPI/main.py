from fastapi import FastAPI
import random

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/antarctica")
async def antarctica():
    return {"temperature": round(random.uniform(-89.2, 15), 2)}


@app.get("/deathvalley")
async def deathvalley():
    return {"temperature": round(random.uniform(2, 57), 2)}


@app.get("/saaradesert")
async def saaradesert():
    return {"temperature": round(random.uniform(-4, 47), 2)}
