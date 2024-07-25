#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from starlette.status import HTTP_401_UNAUTHORIZED
from sqlalchemy.orm import Session
from myapp.database import get_db
from myapp.core.security import (
    create_access_token,
    authenticate_user,
    get_current_user,
    auth_scheme,
)
from myapp.schema.user import UserCreate, UserLogin
from myapp.database.user import User, create_user
from myapp.schema.user import UserCreate, UserResponse
import bcrypt

router = APIRouter()


@router.post("/register", response_model=UserResponse, name="register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists",
        )

    # Create the user if not exists
    db_user = create_user(db, user)
    return db_user


@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(user.email, user.password)
    if not db_user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
def get_current_user_route(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    user_email = get_current_user(token.credentials)
    return {"email": user_email}
