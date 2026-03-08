from fastapi.security import HTTPBearer
from jose import jwt
from fastapi import Depends

from auth import ALGORITHM, SECRET_KEY

security = HTTPBearer()


def get_current_user(token=Depends(security)):

    payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])

    return payload["sub"]