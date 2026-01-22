from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
import os

def register_middleware(app: FastAPI):

    @app.middleware("http")
    async def jwt_middleware(request: Request, call_next):

        JWT_SECRET = os.getenv("JWT_SECRET")  # BURAYA TAŞI

        if not JWT_SECRET:
            return JSONResponse(
                status_code=500,
                content={"detail": "JWT_SECRET not loaded"}
            )

        if request.url.path in ["/", "/docs", "/openapi.json"]:
            return await call_next(request)

        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Missing token"})

        token = auth.split()[1]

        try:
            decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            request.state.user = decoded

        except ExpiredSignatureError:
            return JSONResponse(status_code=401, content={"detail": "Token expired"})
        except JWTError as e:
            print("JWT decode error:", e)
            return JSONResponse(status_code=401, content={"detail": "Invalid token!!"})

        return await call_next(request)
