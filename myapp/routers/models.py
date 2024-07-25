#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
import hashlib
from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials
from myapp.schema.models import TransformerModelInput, TransformerModelLoader
from myapp.tasks.models import load_model_task
from myapp.core.config import DEFAULT_MODEL_PATH
from myapp.core.security import validate_token, auth_scheme


router = APIRouter()

default_model = TransformerModelInput(
    model_name=DEFAULT_MODEL_PATH, tokenizer_name=None
)


@router.post("/load_model")
def load_model(
    background_tasks: BackgroundTasks,
    request: Request,
    model: TransformerModelInput = default_model.copy(),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    # Validate the Bearer token
    validate_token(token.credentials)

    model_name = model.mdl_name
    tokenizer_name = model.tokenizer_name or model_name
    model_id = hashlib.md5(f"{model_name}-{tokenizer_name}".encode()).hexdigest()

    if model_id in request.app.state.models:
        return JSONResponse({"model_id": model_id, "message": "Model already loaded."})

    background_tasks.add_task(
        load_model_task, request.app, model_id, model_name, tokenizer_name
    )
    return JSONResponse({"model_id": model_id, "message": "Model loading initiated."})


@router.post("/unload_model")
def unload_model(
    model: TransformerModelLoader,
    request: Request,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    # Validate the Bearer token
    validate_token(token.credentials)

    model_id = model.mdl_id
    if model_id in request.app.state.models:
        request.app.state.models[model_id] = None
        del request.app.state.models[model_id]
        return JSONResponse({"message": "Model unloaded successfully."})
    else:
        raise HTTPException(status_code=404, detail="Model ID not found.")


@router.get("/get_model")
def get_model(
    model_id: str,
    request: Request,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    # Validate the Bearer token
    validate_token(token.credentials)

    if model_id in request.app.state.models:
        return JSONResponse({"model_id": model_id, "message": "Model is loaded."})
    else:
        raise HTTPException(status_code=404, detail="Model ID not found.")
