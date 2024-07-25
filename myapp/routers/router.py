#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter
from myapp.routers import classify, user
from myapp.routers import models


# Create the main APIRouter instance
api_router = APIRouter()

# Include prediction routes with a prefix
api_router.include_router(classify.router, tags=["prediction"], prefix="/prediction")
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(models.router, prefix="/models", tags=["models"])
