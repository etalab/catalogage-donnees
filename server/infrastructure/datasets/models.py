import uuid
from typing import List

from sqlalchemy import (
    Column,
    Computed,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
)
from sqlalchemy.dialects.postgresql import ARRAY, TSVECTOR, UUID
from sqlalchemy.orm import Mapped, relationship

from server.domain.datasets.entities import (
    DataFormat,
    GeographicalCoverage,
    UpdateFrequency,
)

from ..catalog_records.repositories import CatalogRecordModel
from ..database import Base, mapper_registry
from ..tags.repositories import TagModel, dataset_tag

# Association table
# See: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#many-to-many
dataset_dataformat = Table(
    "dataset_dataformat",
    mapper_registry.metadata,
    Column("dataset_id", ForeignKey("dataset.id"), primary_key=True),
    Column("dataformat_id", ForeignKey("dataformat.id"), primary_key=True),
)


class DataFormatModel(Base):
    __tablename__ = "dataformat"

    id = Column(Integer, primary_key=True)
    name = Column(Enum(DataFormat, name="dataformat_enum"), nullable=False, unique=True)

    datasets: List["DatasetModel"] = relationship(
        "DatasetModel",
        back_populates="formats",
        secondary=dataset_dataformat,
    )


class DatasetModel(Base):
    __tablename__ = "dataset"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True)

    catalog_record: "CatalogRecordModel" = relationship(
        "CatalogRecordModel",
        back_populates="dataset",
        cascade="delete",
        lazy="joined",
        uselist=False,
    )

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    service = Column(String, nullable=False)
    geographical_coverage = Column(
        Enum(GeographicalCoverage, enum="geographical_coverage_enum"), nullable=False
    )
    formats: List[DataFormatModel] = relationship(
        "DataFormatModel",
        back_populates="datasets",
        secondary=dataset_dataformat,
    )
    technical_source = Column(String)
    producer_email = Column(String, nullable=False)
    contact_emails = Column(ARRAY(String), server_default="{}", nullable=False)
    update_frequency = Column(Enum(UpdateFrequency, enum="update_frequency_enum"))
    last_updated_at = Column(DateTime(timezone=True))
    published_url = Column(String)
    tags: List["TagModel"] = relationship(
        "TagModel", back_populates="datasets", secondary=dataset_tag
    )

    search_tsv: Mapped[str] = Column(
        TSVECTOR,
        Computed("to_tsvector('french', title || ' ' || description)", persisted=True),
    )

    __table_args__ = (
        Index(
            "ix_dataset_search_tsv",
            search_tsv,
            postgresql_using="GIN",
        ),
    )
