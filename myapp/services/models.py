#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
import logging
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from transformers import pipeline
from myapp.schema.classify import (
    ZeroClassificationInput,
    ZeroClassificationOutput,
)

logger = logging.getLogger(__name__)


class ZeroShotTextClassifier:
    def __init__(
        self,
        model_name: str = "typeform/mobilebert-uncased-mnli",
        tokenizer_name: str | None = None,
        max_length: int = 512,
        device: str = "cuda",
    ) -> None:
        self.model_name = model_name
        self.max_length = max_length
        self.tokenizer_name = (
            tokenizer_name if tokenizer_name is not None else model_name
        )
        self.device = device
        self._load_model()

    def _load_model(self) -> None:
        logger.debug(f"Loading model {self.model_name}.")
        tokenizer = AutoTokenizer.from_pretrained(
            self.tokenizer_name, model_max_length=self.max_length
        )
        model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        try:
            self.classifier = pipeline(
                "zero-shot-classification",
                model=model,
                tokenizer=tokenizer,
                device=self.device,
            )
        except Exception as e:
            logger.error(f"Error loading model {self.model_name}: {e}")
            raise

    def _pre_process(self, payload: ZeroClassificationInput) -> dict:
        logger.debug("Pre-processing payload.")
        return {"text": payload.text, "candidate_labels": payload.candidate_labels}

    def _post_process(self, prediction: dict) -> ZeroClassificationOutput:
        logger.debug("Post-processing prediction.")
        return ZeroClassificationOutput(
            labels=prediction["labels"], scores=prediction["scores"]
        )

    def _predict(self, features: dict) -> dict:
        logger.debug("Predicting.")
        try:
            return self.classifier(
                features["text"],
                features["candidate_labels"],
                max_length=self.max_length,
            )

        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            raise

    def predict(self, payload: ZeroClassificationInput) -> ZeroClassificationOutput:
        pre_processed_payload = self._pre_process(payload)
        prediction = self._predict(pre_processed_payload)
        post_processed_result = self._post_process(prediction)
        logger.info("Prediction successful.")
        return post_processed_result
