from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


# =========================================================
# TRANSACTION
# =========================================================

class TransactionCreate(BaseModel):

    transaction_id: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    amount: Decimal = Field(
        ...,
        gt=0
    )

    currency: str = Field(
        ...,
        min_length=3,
        max_length=3
    )

    source: str = Field(
        ...,
        min_length=1
    )

    status: str = Field(
        ...,
        min_length=1
    )

    transaction_time: datetime

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, value):

        value = value.upper()

        allowed_currencies = {
            "GBP",
            "USD",
            "EUR",
            "INR"
        }

        if value not in allowed_currencies:

            raise ValueError(
                "Currency must be GBP, USD, EUR, or INR"
            )

        return value

    @field_validator("source")
    @classmethod
    def validate_source(cls, value):

        allowed_sources = {
            "bank",
            "payment_system"
        }

        if value not in allowed_sources:

            raise ValueError(
                "Source must be bank or payment_system"
            )

        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):

        allowed_statuses = {
            "pending",
            "completed",
            "failed"
        }

        value = value.lower()

        if value not in allowed_statuses:

            raise ValueError(
                "Status must be pending, completed, or failed"
            )

        return value


# =========================================================
# LOGIN
# =========================================================

class LoginRequest(BaseModel):

    username: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    password: str = Field(
        ...,
        min_length=1,
        max_length=255
    )