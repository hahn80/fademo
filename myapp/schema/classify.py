#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import List


class ZeroClassificationInput(BaseModel):
    text: str
    candidate_labels: List[str]


class ZeroClassificationOutput(BaseModel):
    labels: List[str]
    scores: List[float]
