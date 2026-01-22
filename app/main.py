import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from app.middleware import register_middleware

load_dotenv()

app = FastAPI()
register_middleware(app)

messages = [
    {"id": 1, "user_id": 1, "text": "Welcome to the platform!"},
    {"id": 2, "user_id": 2, "text": "Your report is ready for download."},
    {"id": 3, "user_id": 1, "text": "You have a new notification."},
    {"id": 4, "user_id": 3, "text": "Password will expire in 5 days."},
    {"id": 5, "user_id": 2, "text": "New login detected from a new device."},
    {"id": 6, "user_id": 3, "text": "Your subscription has been updated."}
]

@app.get("/")
def read_root():
    return {"msg": "Open endpoint"}

@app.get("/protected")
def protected(request: Request):
    return {"msg": "For authorized users only", "authorizedUser": request.state.user}

@app.get("/messages")
def get_messages(request: Request):
    user = request.state.user
    role = user.get("role")
    sub = user.get("sub")

    if role == "admin":
        return messages
    else:
        # sub integer değilse dönüştür
        if isinstance(sub, str) and sub.isdigit():
            sub = int(sub)
        return [m for m in messages if m["user_id"] == sub]
