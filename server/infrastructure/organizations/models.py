from sqlalchemy import CHAR, Column, String

from server.domain.organizations.types import Siret

from ..database import Base


class OrganizationModel(Base):
    __tablename__ = "organization"

    siret: Siret = Column(CHAR(14), primary_key=True)
    name: str = Column(String(), nullable=False)
