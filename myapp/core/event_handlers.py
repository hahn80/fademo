#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from typing import Callable
from contextlib import asynccontextmanager
from fastapi import FastAPI


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Running app start handler.")
    app.state.models = {}
    yield
    # Clean up the ML models and release the resources
    logger.info("Running app shutdown handler.")
    for model_id in app.state.models:
        if app.state.models[model_id] is not None:
            app.state.models[model_id] = None
    app.state.models = None


def start_app_handler(app: FastAPI) -> Callable:
    def startup() -> None:
        logger.info("Running app start handler.")
        app.state.models = {}  # Initialize empty dictionary for models

    return startup


def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        logger.info("Running app shutdown handler.")
        # Loop over the dictionary of models and unload each one
        for model_id in app.state.models:
            if app.state.models[model_id] is not None:
                app.state.models[model_id] = None
        app.state.models = None  # Clear the models dictionary on shutdown

    return shutdown
