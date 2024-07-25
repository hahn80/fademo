#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from myapp.services.models import ZeroShotTextClassifier


def load_model_task(app, model_id, model_name, tokenizer_name):
    model = ZeroShotTextClassifier(model_name=model_name, tokenizer_name=tokenizer_name)
    app.state.models[model_id] = model
