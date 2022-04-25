from fastapi import FastAPI
import random

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/antarctica")
async def antarctica():
    print("--------------------------------------------------------------", file =  open('api_log.txt','a'))
    print("Requisicao de nova temperatura para Antartica recebida", file =  open('api_log.txt','a'))
    return {"temperature": round(random.uniform(-89.2, 15), 2)}


@app.get("/deathvalley")
async def deathvalley():
    print("--------------------------------------------------------------", file =  open('api_log.txt','a'))
    print("Requisicao de nova temperatura para Vale da Morte recebida", file =  open('api_log.txt','a'))
    return {"temperature": round(random.uniform(2, 57), 2)}


@app.get("/saaradesert")
async def saaradesert():
    print("--------------------------------------------------------------", file =  open('api_log.txt','a'))
    print("Requisicao de nova temperatura para Deserto do Saara recebida", file =  open('api_log.txt','a'))
    return {"temperature": round(random.uniform(-4, 47), 2)}
