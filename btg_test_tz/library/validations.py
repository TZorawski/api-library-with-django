from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import re

class BookCreateSchema(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    author: str = Field(min_length=1, max_length=255)
    publication_year: int = Field(ge=0)
    edition: Optional[int] = Field(None, ge=0)
    isbn: str = Field(min_length=10, max_length=13)
    total_copies: int = Field(ge=0)

    @field_validator("publication_year")
    @classmethod
    def validate_publication_year(cls, value: int):
        current_year = datetime.now().year
        if value > current_year:
            raise ValueError("publication_year cannot be in the future")
        return value

    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, value: str):
        if not value.isdigit():
            raise ValueError("ISBN must contain only numbers")
        return value
    
class BookUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    author: Optional[str] = Field(None, min_length=1, max_length=255)
    publication_year: Optional[int] = Field(None, ge=0)
    edition: Optional[int] = Field(None, ge=0)
    isbn: Optional[str] = Field(None, min_length=10, max_length=13)
    total_copies: Optional[int] = Field(None, ge=0)

    @field_validator("publication_year")
    @classmethod
    def validate_publication_year(cls, value: Optional[int]):
        if value is None:
            return value

        current_year = datetime.now().year
        if value > current_year:
            raise ValueError("Publication year cannot be in the future")
        return value

    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, value: Optional[str]):
        if value is None:
            return value

        if not value.isdigit():
            raise ValueError("ISBN must contain only numbers")
        return value
    
class UserCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    email: str = Field(min_length=1, max_length=254)
    cpf: str = Field(min_length=11, max_length=11)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str):
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        if not re.match(regex, value):
            raise ValueError("Email address is invalid.")
        return value

    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, value: str):
        if not value.isdigit():
            raise ValueError("CPF must contain only numbers")
        return value
    
class UserUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[str] = Field(None, min_length=1, max_length=254)
    cpf: Optional[str] = Field(None, min_length=11, max_length=11)
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, value: Optional[str]):
        if value is None:
            return value
        
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        if not re.match(regex, value):
            raise ValueError("Email address is invalid.")
        return value

    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, value: Optional[str]):
        if value is None:
            return value
        
        if not value.isdigit():
            raise ValueError("CPF must contain only numbers")
        return value