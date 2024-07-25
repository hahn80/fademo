#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from sqlalchemy import Column, Integer, String
from myapp.database import Base
from myapp.schema.user import UserCreate
from sqlalchemy.orm import Session
import bcrypt


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    db_user = User(email=user.email, hashed_password=hashed_password.decode("utf-8"))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
