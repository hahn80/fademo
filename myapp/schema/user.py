#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from pydantic import BaseModel, EmailStr, ConfigDict


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr

    # class Config:
    #     from_attributes = True
