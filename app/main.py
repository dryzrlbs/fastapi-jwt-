import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from app.middleware import register_middleware

# .env yükle
load_dotenv()

# FastAPI uygulaması
app = FastAPI()

# JWT middleware register
register_middleware(app)

# Açık endpoint
@app.get("/")
def read_root():
    return {"msg": "Open endpoint"}

# Protected endpoint (tüm doğrulama JWT middleware tarafından yapılır)
@app.get("/protected")
def protected(request: Request):
    return {
        "msg": "For authorized users only",
        "authorizedUser": request.state.user
    }


MESSAGES = [
    { "id": 1, "user_id": 1, "text": "Welcome to the platform!" },
    { "id": 2, "user_id": 2, "text": "Your report is ready for download." },
    { "id": 3, "user_id": 1, "text": "You have a new notification." },
    { "id": 4, "user_id": 3, "text": "Password will expire in 5 days." },
    { "id": 5, "user_id": 2, "text": "New login detected from a new device." },
    { "id": 6, "user_id": 3, "text": "Your subscription has been updated." }
]

# /messages endpoint
@app.get("/messages")
def get_messages(request: Request):
    user = request.state.user
    role = user.get("role")
    sub = user.get("sub")

    if role == "admin":
        # admin can see all messages
        return MESSAGES

    # normal users see only their messages
    return [msg for msg in MESSAGES if msg["user_id"] == sub]
