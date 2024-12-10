from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    firstname = Column(String(45), nullable=False)
    lastname = Column(String(45), nullable=False)
    email = Column(String(45), nullable=False, unique=True)
    country = Column(String(45), nullable=False)
    city = Column(String(45), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __init__(self, firstname, lastname, email, country, city) -> None:
        super().__init__()
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.country = country
        self.city = city

    def __repr__(self) -> str:
        return super().__repr__() + '\n\nFirst Name: {firstname}\nLast Name: {lastname}\nEmail: {email}\nCountry: {country}\nCity: {city}\n'.format(firstname=self.firstname, lastname=self.lastname, email=self.email, country=self.country, city=self.city)
