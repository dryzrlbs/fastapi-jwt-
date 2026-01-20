import os
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from dotenv import load_dotenv

# .env yükle
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"  # Şimdilik tek algoritma

def register_middleware(app: FastAPI):
    @app.middleware("http")
    async def jwt_middleware(request: Request, call_next):
        # Açık endpointler (token gerekmiyor)
        open_paths = ["/"]
        if request.url.path in open_paths:
            return await call_next(request)

        # Authorization header kontrolü
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing or invalid Authorization header"}
            )

        # Token decode
        token = auth_header.split()[1]
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            request.state.user = payload  # role ve sub buradan okunacak
        except ExpiredSignatureError:
            return JSONResponse(status_code=401, content={"detail": "Token expired"})
        except JWTError as e:
            # Güvenlik için hatayı client’a detaylı vermiyoruz
            print(f"JWT decode error: {e}")
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})

        # Token geçerliyse devam et
        response = await call_next(request)
        return response
