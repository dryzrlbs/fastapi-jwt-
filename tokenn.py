from jose import jwt
import os

# .env dosyandaki secret ile aynı
JWT_SECRET = "a-string-secret-at-least-256-bits-long"
ALGORITHM = "HS256"


payloads = [
    {"sub": "1", "name": "Alice", "role": "user"},
    {"sub": "2", "name": "Bob", "role": "user"},
    {"sub": "3", "name": "Carol", "role": "admin"}
]


for user in payloads:
    token = jwt.encode(user, JWT_SECRET, algorithm=ALGORITHM)
    print(f"{user['name']} token: {token}")
