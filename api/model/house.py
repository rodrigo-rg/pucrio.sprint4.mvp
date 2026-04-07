from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from typing import Union
from model import Base

# Colunas: SquareFeet, Bedrooms, Bathrooms, Neighborhood, YearBuilt, Price_Range

class House(Base):
    __tablename__ = 'casas'
    
    id = Column(Integer, primary_key=True)
    address = Column("Address", String(100))
    square_feet = Column("SquareFeet", Integer)
    bedrooms = Column("Bedrooms", Integer)
    bathrooms = Column("Bathrooms", Integer)
    neighborhood = Column("Neighborhood", Integer)
    year_built = Column("YearBuilt", Integer)
    price_range = Column("Price_Range", Integer, nullable=True)
    data_insercao = Column(DateTime, default=datetime.now())
    
    def __init__(self, address: str, square_feet: int, bedrooms: int,
                 bathrooms: int, neighborhood: int, year_built: int,
                 price_range: int = None,
                 data_insercao: Union[DateTime, None] = None):
        """
        Cria um registro de Casa

        Arguments:
            address: endereço da casa
            square_feet: tamanho da casa em pés quadrados
            bedrooms: número de quartos
            bathrooms: número de banheiros
            neighborhood: tipo de vizinhança (1=Rural, 2=Urban, 3=Suburb)
            year_built: ano de construção
            price_range: faixa de preço predita (de 1 a 9)
            data_insercao: data de quando a casa foi inserida na base
        """
        self.address = address
        self.square_feet = square_feet
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.neighborhood = neighborhood
        self.year_built = year_built
        self.price_range = price_range
        self.data_insercao = data_insercao
