from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def read_all_books():
    return {'message': 'Hello world!'}