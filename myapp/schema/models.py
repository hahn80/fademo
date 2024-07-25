#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class TransformerModelInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    # Prefix model_ is protected by Pydantic -> use mdl_
    mdl_name: str = Field(alias="model_name")
    tokenizer_name: Optional[str] = None

    # class Config:
    #     populate_by_name = True


class TransformerModelLoader(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    mdl_id: str = Field(alias="model_id")

    # class Config:
    #     populate_by_name = True
