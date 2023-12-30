from fastapi import Form

from uidom.dom import *
from uidom.elements import *

__all__ = ["get", "post", "check_user"]


@TextInput(
    name="username",
    placeholder="User",
    className="flex form-input rounded-md overflow-hidden p-2 ",
)
def text_input(*args, **kwargs):
    return attr(*args, **kwargs)


@PasswordInput(
    name="password",
    placeholder="Password",
    className="flex form-input rounded-md overflow-hidden p-2 ",
)
def password_input(*args, **kwargs):
    return attr(*args, **kwargs)


users = dict(user1={"password": ""})


def get():
    with form(hx_post="/login", className="space-y-2 m-2") as login_form:
        HiddenInput(name="token", placeholder=None)
        text_input(id="username", hx_get="/login/check_user", hx_target="#user_msg")
        div(id="user_msg")
        password_input(id="password")
        SubmitButton(label="Submit", value="submit")
    return login_form


def check_user(username: str):
    if username in users:
        return Fragment()
    return div(f"{username} not present")


def post(username: str = Form(...), password: str = Form(...), token: str = Form(...)):
    return div(username, password)
