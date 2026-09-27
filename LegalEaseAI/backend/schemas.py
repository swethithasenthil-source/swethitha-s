from typing import Literal

from pydantic import BaseModel, Field, field_validator


class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2, max_length=120)
    parties: str = Field(..., min_length=2, max_length=3000)
    terms: str = Field(..., min_length=2, max_length=10000)
    effective_date: str = Field(..., min_length=2, max_length=100)

    @field_validator(
        "document_type",
        "parties",
        "terms",
        "effective_date",
    )
    @classmethod
    def strip_values(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError("This field cannot be empty.")

        return value


class GenerateResponse(BaseModel):
    document_type: str
    text: str
    terms: list[str]


class ExportRequest(BaseModel):
    document_type: str = Field(..., min_length=2, max_length=120)
    text: str = Field(..., min_length=2, max_length=100000)
    terms: list[str] = Field(default_factory=list, max_length=100)
    format: Literal["txt", "docx", "pdf"]
    logo_base64: str | None = None