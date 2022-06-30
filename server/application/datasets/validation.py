from typing import List, Optional

from pydantic import BaseModel, validator

from server.domain.datasets.entities import DataFormat


class CreateDatasetValidationMixin(BaseModel):
    @validator("formats", check_fields=False)
    def check_formats_at_least_one(cls, value: List[DataFormat]) -> List[DataFormat]:
        if not value:
            raise ValueError("formats must contain at least one item")
        return value

    @validator("contact_emails", check_fields=False)
    def check_contact_emails_at_least_one(cls, value: List[str]) -> List[str]:
        if not value:
            raise ValueError("contact_emails must contain at least one item")
        return value


class UpdateDatasetValidationMixin(BaseModel):
    @validator("title", check_fields=False)
    def check_title_not_empty(cls, value: str) -> str:
        if not value:
            raise ValueError("title must not be empty")
        return value

    @validator("description", check_fields=False)
    def check_description_not_empty(cls, value: str) -> str:
        if not value:
            raise ValueError("description must not be empty")
        return value

    @validator("service", check_fields=False)
    def check_service_not_empty(cls, value: str) -> str:
        if not value:
            raise ValueError("service must not be empty")
        return value

    @validator("formats", check_fields=False)
    def check_formats_at_least_one(cls, value: List[DataFormat]) -> List[DataFormat]:
        if not value:
            raise ValueError("formats must contain at least one item")
        return value

    @validator("contact_emails", check_fields=False)
    def check_contact_emails_at_least_one(cls, value: List[str]) -> List[str]:
        if not value:
            raise ValueError("contact_emails must contain at least one item")
        return value

    @validator("published_url", check_fields=False)
    def check_published_url_not_empty(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value:
            raise ValueError("published_url must not be empty")
        return value
