from datetime import datetime, timedelta
from jose import JWTError, jwt, ExpiredSignatureError


SECRET_KEY = "secret_key_change_this"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10000000


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


from datetime import datetime

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Token payload:", payload)
        return payload
    except ExpiredSignatureError:
        print("Token expired")
        return None
    except JWTError as e:
        print(f"JWT decode error: {e}")
        print("Received token:", token)
        return None
