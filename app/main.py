from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get('/', response_class=HTMLResponse)
@app.get('/index', response_class=HTMLResponse)
def index():
    return 'Hello, World!'