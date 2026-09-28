from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    profile = relationship(
        "Profile",
        back_populates="user",
        uselist=False
    )


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    phone = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    bio = Column(Text, nullable=True)

    user = relationship(
        "User",
        back_populates="profile"
    )
