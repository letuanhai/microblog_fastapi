from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
@app.get("/index", response_class=HTMLResponse)
def index(
    request: Request,
):
    user = {"username": "hai"}
    posts = [
        {"author": {"username": "John"}, "body": "Beautiful day in Portland!"},
        {"author": {"username": "Susan"}, "body": "The Avengers movie was so cool!"},
    ]
    return templates.TemplateResponse(
        request=request,
        name="index.jinja-html",
        context=dict(title="Home", user=user, posts=posts),
    )
