from sqlalchemy import Column, Integer, String

from server.db import Base


class Dataset(Base):
    __tablename__ = "dataset"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
