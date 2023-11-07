from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BLOB
from sqlalchemy.orm import relationship

from .database import Base


class Floor(Base):
    __tablename__ = "floor"

    id = Column(Integer, primary_key=True, index=True)
    image = Column(BLOB, index=True)


class Camera(Base):
    __tablename__ = "camera"

    id = Column(Integer, primary_key=True, index=True)
    c_x1 = Column(Integer, index=True)
    c_y1 = Column(Integer, index=True)
    c_x2 = Column(Integer, index=True)
    c_y2 = Column(Integer, index=True)
    c_x3 = Column(Integer, index=True)
    c_y3 = Column(Integer, index=True)
    c_x4 = Column(Integer, index=True)
    c_y4 = Column(Integer, index=True)
    f_x1 = Column(Integer, index=True)
    f_y1 = Column(Integer, index=True)
    f_x2 = Column(Integer, index=True)
    f_y2 = Column(Integer, index=True)
    f_x3 = Column(Integer, index=True)
    f_y3 = Column(Integer, index=True)
    f_x4 = Column(Integer, index=True)
    f_y4 = Column(Integer, index=True)

    floor_id = Column(Integer, ForeignKey("floor.id"))
    in_floor = relationship("floor", back_populates="items")