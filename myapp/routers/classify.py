#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials
from myapp.core.security import validate_token, auth_scheme
from myapp.schema.classify import ZeroClassificationInput, ZeroClassificationOutput
from myapp.schema.models import TransformerModelLoader
from myapp.services.models import ZeroShotTextClassifier


router = APIRouter()


default_data = ZeroClassificationInput(
    text="I have a problem with my iPhone that needs to be resolved asap!",
    candidate_labels=["urgent", "not urgent", "phone", "tablet", "computer"],
).dict()


@router.post("/classify", response_model=ZeroClassificationOutput, name="classify")
def classify(
    loader: TransformerModelLoader,
    request: Request,
    data: ZeroClassificationInput = default_data.copy(),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> ZeroClassificationOutput:
    # Validate the Bearer token
    validate_token(token.credentials)

    model_id = loader.mdl_id
    if (
        model_id not in request.app.state.models
        or request.app.state.models[model_id] is None
    ):
        raise HTTPException(status_code=404, detail="Model not found or not loaded")

    classifier: ZeroShotTextClassifier = request.app.state.models[model_id]

    # Perform classification using ZeroShotTextClassifier
    prediction: ZeroClassificationOutput = classifier.predict(data)

    return prediction
