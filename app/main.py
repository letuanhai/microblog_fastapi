from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette_wtf import CSRFProtectMiddleware, csrf_protect

from app.forms import LoginForm
from app.utils import get_flashed_messages, flash
from config import Config

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=Config.SECRET_KEY)
app.add_middleware(
    CSRFProtectMiddleware,
    csrf_secret=Config.SECRET_KEY,  # use bytestring cause token signature to be invalid # type: ignore
)

templates = Jinja2Templates(directory="app/templates")
templates.env.globals["get_flashed_messages"] = get_flashed_messages


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


@app.get("/login")
@app.post("/login")
@csrf_protect
async def login(request: Request):
    form = await LoginForm.from_formdata(request=request)
    print(f"Form: {form.data}")

    if await form.validate_on_submit():
        flash(
            request=request,
            message=f"Login requested for user {form.username.data}, remember_me={form.remember_me.data}",
        )
        return RedirectResponse(
            url=request.url_for("index"), status_code=status.HTTP_302_FOUND
        )
    return templates.TemplateResponse(
        request=request, name="login.jinja-html", context=dict(form=form)
    )
