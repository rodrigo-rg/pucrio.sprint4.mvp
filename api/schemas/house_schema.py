from pydantic import BaseModel
from typing import Optional, List
from model.house import House
import json
import numpy as np

class HouseSchema(BaseModel):
    """Define como uma nova casa a ser inserida deve ser representada"""
    address: str = "Rua das Oliveiras, 123"
    square_feet: int = 2126
    bedrooms: int = 4
    bathrooms: int = 1
    neighborhood: int = 1
    year_built: int = 1969
    
class HouseViewSchema(BaseModel):
    """Define como uma casa será retornada"""
    id: int = 1
    address: str = "Rua das Oliveiras, 123"
    square_feet: int = 2126
    bedrooms: int = 4
    bathrooms: int = 1
    neighborhood: int = 1
    year_built: int = 1969
    price_range: int = None
    
class HouseBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no endereço da casa.
    """
    address: str = "Rua das Oliveiras, 123"

class ListaCasasSchema(BaseModel):
    """Define como uma lista de casas será representada"""
    casas: List[HouseSchema]

    
class HouseDelSchema(BaseModel):
    """Define como uma casa para deleção será representada"""
    address: str = "Rua das Oliveiras, 123"
    
# Apresenta apenas os dados de uma casa    
def apresenta_casa(house: House):
    """Retorna uma representação da casa seguindo o schema definido em
        HouseViewSchema.
    """
    return {
        "id": house.id,
        "address": house.address,
        "square_feet": house.square_feet,
        "bedrooms": house.bedrooms,
        "bathrooms": house.bathrooms,
        "neighborhood": house.neighborhood,
        "year_built": house.year_built,
        "price_range": house.price_range
    }
    
# Apresenta uma lista de casas
def apresenta_casas(houses: List[House]):
    """Retorna uma representação da lista de casas seguindo o schema definido em
        HouseViewSchema.
    """
    result = []
    for house in houses:
        result.append({
            "id": house.id,
            "address": house.address,
            "square_feet": house.square_feet,
            "bedrooms": house.bedrooms,
            "bathrooms": house.bathrooms,
            "neighborhood": house.neighborhood,
            "year_built": house.year_built,
            "price_range": house.price_range
        })

    return {"casas": result}
