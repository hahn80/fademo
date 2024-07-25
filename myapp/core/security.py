#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bcrypt
from datetime import datetime, timedelta, timezone
from myapp import jwt
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from starlette.status import HTTP_401_UNAUTHORIZED
from myapp.core.config import SECRET_KEY, ALGORITHM
from myapp.database.user import User
from myapp.database import SessionLocal


auth_scheme = HTTPBearer()


# Function to create JWT token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = (
        datetime.now(tz=timezone.utc) + expires_delta
    )  # Use UTC time for consistency
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Function to authenticate user
def authenticate_user(email: str, password: str):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    if not user or not bcrypt.checkpw(
        password.encode("utf-8"), user.hashed_password.encode("utf-8")
    ):
        return False
    return user


# Function to get current user from JWT token
def get_current_user(token: str):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    return email


def validate_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.DecodeError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
