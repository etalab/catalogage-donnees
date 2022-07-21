from typing import TYPE_CHECKING, List

from sqlalchemy import CHAR, Column, String
from sqlalchemy.orm import relationship

from server.domain.organizations.types import Siret

from ..database import Base

if TYPE_CHECKING:
    from ..auth.repositories import UserModel
    from ..catalogs.models import CatalogModel


class OrganizationModel(Base):
    __tablename__ = "organization"

    siret: Siret = Column(CHAR(14), primary_key=True)
    name: str = Column(String(), nullable=False)

    catalog: "CatalogModel" = relationship(
        "CatalogModel",
        back_populates="organization",
        uselist=False,
    )

    users: List["UserModel"] = relationship(
        "UserModel",
        back_populates="organization",
    )
