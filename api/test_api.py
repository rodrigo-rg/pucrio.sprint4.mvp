import pytest
import json
from app import app
from model import Session, House

# To run: pytest -v test_api.py

@pytest.fixture
def client():
    """Configura o cliente de teste para a aplicação Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_house_data():
    """Dados de exemplo para teste de casa"""
    return {
        "address": "Rua das Oliveiras, 123",
        "square_feet": 2126,
        "bedrooms": 4,
        "bathrooms": 1,
        "neighborhood": 1,
        "year_built": 1969
    }

def test_home_redirect(client):
    """Testa se a rota home redireciona para o frontend"""
    response = client.get('/')
    assert response.status_code == 302
    assert '/front/index.html' in response.location

def test_docs_redirect(client):
    """Testa se a rota docs redireciona para openapi"""
    response = client.get('/docs')
    assert response.status_code == 302
    assert '/openapi' in response.location

def test_get_casas_empty(client):
    """Testa a listagem de casas quando não há nenhuma"""
    response = client.get('/casas')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'casas' in data
    assert isinstance(data['casas'], list)

def test_add_house_prediction(client, sample_house_data):
    """Testa a adição de uma casa com predição"""
    # Primeiro, vamos limpar qualquer casa existente com o mesmo endereço
    session = Session()
    existing_house = session.query(House).filter(House.address == sample_house_data['address']).first()
    if existing_house:
        session.delete(existing_house)
        session.commit()
    session.close()
    
    # Agora testamos a adição
    response = client.post('/casa', 
                          data=json.dumps(sample_house_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # Verifica se a casa foi criada com todas as informações
    assert data['address'] == sample_house_data['address']
    assert data['square_feet'] == sample_house_data['square_feet']
    assert data['bedrooms'] == sample_house_data['bedrooms']
    assert data['bathrooms'] == sample_house_data['bathrooms']
    assert data['neighborhood'] == sample_house_data['neighborhood']
    assert data['year_built'] == sample_house_data['year_built']
    
    # Verifica se a predição foi feita (price_range deve estar presente)
    assert 'price_range' in data
    assert data['price_range'] in range(1, 10)  # Deve estar entre 1 e 9

def test_add_duplicate_house(client, sample_house_data):
    """Testa a adição de uma casa duplicada"""
    # Primeiro adiciona a casa
    client.post('/casa', 
                data=json.dumps(sample_house_data),
                content_type='application/json')
    
    # Tenta adicionar novamente
    response = client.post('/casa', 
                          data=json.dumps(sample_house_data),
                          content_type='application/json')
    
    assert response.status_code == 409
    data = json.loads(response.data)
    assert 'message' in data
    assert 'já existente' in data['message']

def test_get_house_by_address(client, sample_house_data):
    """Testa a busca de uma casa por endereço"""
    # Primeiro adiciona a casa
    client.post('/casa', 
                data=json.dumps(sample_house_data),
                content_type='application/json')
    
    # Busca a casa por endereço
    response = client.get(f'/casa?address={sample_house_data["address"]}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['address'] == sample_house_data['address']

def test_get_nonexistent_house(client):
    """Testa a busca de uma casa que não existe"""
    response = client.get('/casa?address=EnderecoInexistente')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'message' in data

def test_delete_house(client, sample_house_data):
    """Testa a remoção de uma casa"""
    # Primeiro adiciona a casa
    client.post('/casa', 
                data=json.dumps(sample_house_data),
                content_type='application/json')
    
    # Remove a casa
    response = client.delete(f'/casa?address={sample_house_data["address"]}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'removida com sucesso' in data['message']

def test_delete_nonexistent_house(client):
    """Testa a remoção de uma casa que não existe"""
    response = client.delete('/casa?address=EnderecoInexistente')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'message' in data

def cleanup_test_houses():
    """Limpa casas de teste do banco"""
    session = Session()
    test_houses = session.query(House).filter(
        House.address.in_(['Rua das Oliveiras, 123', 'Casa Minima', 'Casa Maxima'])
    ).all()
    
    for house in test_houses:
        session.delete(house)
    session.commit()
    session.close()

# Executa limpeza após os testes
def test_cleanup():
    """Limpa dados de teste"""
    cleanup_test_houses()
