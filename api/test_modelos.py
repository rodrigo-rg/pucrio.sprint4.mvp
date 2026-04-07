from model.carregador import Carregador
from model.modelo import Model
from model.avaliador import Avaliador
from model.pipeline import Pipeline
from model import *

# To run: pytest -v test_modelos.py

# Instanciação das Classes
carregador = Carregador()
modelo = Model()
avaliador = Avaliador()
pipeline = Pipeline()

# Parâmetros    
url_dados = "./MachineLearning/data/house_price_dataset.csv"
colunas = ['SquareFeet', 'Bedrooms', 'Bathrooms', 'Neighborhood', 'YearBuilt', 'Price_Range']

# Carga dos dados
dataset = carregador.carregar_dados(url_dados, colunas)
array = dataset.values
X = array[:,0:-1]
y = array[:,-1]
    
# Método para testar o modelo
def test_modelo_house_price():  
    # Importando o pipeline treinado
    path = './MachineLearning/pipelines/lr_house_price_pipeline.pkl'
    modelo = pipeline.carrega_pipeline(path)

    # Obtendo as métricas do modelo
    acuracia = avaliador.avaliar(modelo, X, y)
    
    # Testando as métricas do modelo
    assert acuracia >= 0.35
