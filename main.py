from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return {'data': {'name': 'gopal'}}


@app.get('/data')
def index():
    return {'data': "hello..."}
