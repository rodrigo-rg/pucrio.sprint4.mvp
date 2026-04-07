from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from model.pipeline import Pipeline
from model.preprocessador import PreProcessador
from model.house import House
from model import *
from logger import logger
from schemas import *
from flask_cors import CORS


# Instanciando o objeto OpenAPI
info = Info(title="API House Price Prediction", version="1.0.0")
app = OpenAPI(
    __name__, info=info, static_folder="../front", static_url_path="/front"
)
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(
    name="Documentação",
    description="Seleção de documentação: Swagger, Redoc ou RapiDoc",
)
house_tag = Tag(
    name="Casa",
    description="Adição, visualização, remoção e predição de faixa de preço de casas",
)


# Rota home - redireciona para o frontend
@app.get("/", tags=[home_tag])
def home():
    """Redireciona para o index.html do frontend."""
    return redirect("/front/index.html")


# Rota para documentação OpenAPI
@app.get("/docs", tags=[home_tag])
def docs():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect("/openapi")


# Rota de listagem de casas
@app.get(
    "/casas",
    tags=[house_tag],
    responses={"200": HouseViewSchema, "404": ErrorSchema},
)
def get_casas():
    """Lista todas as casas cadastradas na base
    Args:
       none

    Returns:
        list: lista de casas cadastradas na base
    """
    logger.debug("Coletando dados sobre todas as casas")
    # Criando conexão com a base
    session = Session()
    # Buscando todas as casas
    casas = session.query(House).all()

    if not casas:
        # Se não houver casas
        return {"casas": []}, 200
    else:
        logger.debug(f"%d casas encontradas" % len(casas))
        print(casas)
        return apresenta_casas(casas), 200


# Rota de adição de casa
@app.post(
    "/casa",
    tags=[house_tag],
    responses={
        "200": HouseViewSchema,
        "400": ErrorSchema,
        "409": ErrorSchema,
    },
)
def predict_price(form: HouseSchema):
    """Adiciona uma nova casa à base de dados
    Retorna uma representação da casa e predição de faixa de preço associada.

    """
    # Instanciando classes
    preprocessador = PreProcessador()
    pipeline = Pipeline()

    # Recuperando os dados do formulário
    address = form.address
    square_feet = form.square_feet
    bedrooms = form.bedrooms
    bathrooms = form.bathrooms
    neighborhood = form.neighborhood
    year_built = form.year_built

    # Preparando os dados para o modelo
    X_input = preprocessador.preparar_form(form)
    # Carregando modelo
    model_path = "./MachineLearning/pipelines/lr_house_price_pipeline.pkl"
    modelo = pipeline.carrega_pipeline(model_path)
    # Realizando a predição
    price_range = int(modelo.predict(X_input)[0])

    house = House(
        address=address,
        square_feet=square_feet,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        neighborhood=neighborhood,
        year_built=year_built,
        price_range=price_range,
    )
    logger.debug(f"Adicionando casa no endereço: '{house.address}'")

    try:
        # Criando conexão com a base
        session = Session()

        # Checando se casa já existe na base
        if session.query(House).filter(House.address == form.address).first():
            error_msg = "Casa já existente na base :/"
            logger.warning(
                f"Erro ao adicionar casa '{house.address}', {error_msg}"
            )
            return {"message": error_msg}, 409

        # Adicionando casa
        session.add(house)
        # Efetivando o comando de adição
        session.commit()
        # Concluindo a transação
        logger.debug(f"Adicionada casa no endereço: '{house.address}'")
        return apresenta_casa(house), 200

    # Caso ocorra algum erro na adição
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(
            f"Erro ao adicionar casa '{house.address}', {error_msg}"
        )
        return {"message": error_msg}, 400


# Métodos baseados em endereço
# Rota de busca de casa por endereço
@app.get(
    "/casa",
    tags=[house_tag],
    responses={"200": HouseViewSchema, "404": ErrorSchema},
)
def get_casa(query: HouseBuscaSchema):
    """Faz a busca por uma casa cadastrada na base a partir do endereço

    Args:
        address (str): endereço da casa

    Returns:
        dict: representação da casa e faixa de preço predita
    """

    house_address = query.address
    logger.debug(f"Coletando dados sobre casa no endereço #{house_address}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    house = (
        session.query(House).filter(House.address == house_address).first()
    )

    if not house:
        # se a casa não foi encontrada
        error_msg = f"Casa no endereço {house_address} não encontrada na base :/"
        logger.warning(
            f"Erro ao buscar casa '{house_address}', {error_msg}"
        )
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Casa encontrada: '{house.address}'")
        # retorna a representação da casa
        return apresenta_casa(house), 200


# Rota de remoção de casa por endereço
@app.delete(
    "/casa",
    tags=[house_tag],
    responses={"200": HouseViewSchema, "404": ErrorSchema},
)
def delete_casa(query: HouseBuscaSchema):
    """Remove uma casa cadastrada na base a partir do endereço

    Args:
        address (str): endereço da casa

    Returns:
        msg: Mensagem de sucesso ou erro
    """

    house_address = unquote(query.address)
    logger.debug(f"Deletando dados sobre casa #{house_address}")

    # Criando conexão com a base
    session = Session()

    # Buscando casa
    house = (
        session.query(House).filter(House.address == house_address).first()
    )

    if not house:
        error_msg = "Casa não encontrada na base :/"
        logger.warning(
            f"Erro ao deletar casa '{house_address}', {error_msg}"
        )
        return {"message": error_msg}, 404
    else:
        session.delete(house)
        session.commit()
        logger.debug(f"Deletada casa #{house_address}")
        return {
            "message": f"Casa no endereço {house_address} removida com sucesso!"
        }, 200


if __name__ == "__main__":
    app.run(debug=True)
