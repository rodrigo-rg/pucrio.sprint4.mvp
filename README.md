# MVP da Sprint 4

Sistema para predição de faixas de preço de imóveis utilizando Machine Learning.

O projeto foi desenvolvido utilizando **Python** (backend com Flask) e **HTML/CSS/JavaScript** (frontend).

## Funcionalidades

- **Consultar imóveis** - Listar e buscar casas cadastradas no banco
- **Adicionar imóvel** - Registrar novo imóvel com predição automática de preço
- **Excluir imóvel** - Remover casas do banco de dados
- **Predição de preço do imóvel** - Modelo Machine Learning fornece faixa de preço estimadar.

## Como executar 

### Passo 1: Instalação do Python

Instale o Python versão 3.13 ou superior.

É necessário ir ao diretório raiz dessa aplicação, pelo terminal, para poder executar os comandos descritos abaixo.

### Passo 2 (opcional): Instalação do Ambiente Virtual

Recomenda-se utilizar o ambiente virtual: [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)

Para isso, no terminal, dentro da pasta da api, digite:
```
python -m venv .venv
```

Isso irá criar um ambiente virtual chamado `.venv`.

Talvez seja necessário antes alterar a política de execução do PowerShell para permitir a execução de scripts. Para isso, execute o seguinte comando no PowerShell:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Em seguida, digite o comando abaixo para ativar o ambiente virtual:
```
.\.venv\Scripts\activate
```
Isto irá ativar o ambiente virtual, e você verá o prefixo `(.venv)` no terminal, indicando que o ambiente está ativo.

### Passo 3: Instalação das Dependências

Execute os seguintes comandos:
```
(.venv)$ pip install -r requirements.txt
```
Isso irá instalar as bibliotecas necessárias (Flask, SQLAlchemy, scikit-learn, etc.).

### Passo 4: Executar a API

Execute o seguinte comando:
```
(.venv)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/](http://localhost:5000/) no navegador para acessar a aplicação.

## Documentação da API

- `GET /casas` - Lista todas as casas cadastradas
- `GET /casa` - Busca uma casa pelo endereço
- `POST /casa` - Adiciona uma nova casa e prediz preço
- `DELETE /casa` - Remove uma casa pelo endereço
Consulte a documentação Swagger para detalhes completos dos parâmetros e respostas:
- [Swagger UI](http://localhost:5000/openapi/swagger)

### Pastas e arquivos

**Backend (api/):**
- `database/` - Banco de dados SQLite
- `MachineLearning/` - Módulos e utilitários de Machine Learning
- `model/` - Modelos de Machine Learning, pipeline e processamento de dados
- `schemas/` - Esquemas de validação de dados e serialização
- `app.py` - Aplicação principal Flask com rotas da API
- `logger.py` - Configuração de logging
- `requirements.txt` - Dependências do projeto
- `test_api.py` - Testes unitários da API
- `test_modelos.py` - Testes dos modelos de Machine Learning


## Documentação do Frontend

### Pastas e arquivos

**Frontend (front/):**
- `img/`: Pasta contendo imagens e outros recursos estáticos.
- `index.html`: Página do aplicativo, que é um SPA (Single Page Application).
- `scripts.js`: JavaScript responsável pela lógica do app.
- `styles.css`: Arquivo de estilos CSS.

## Requisitos

- Navegador web moderno (Chrome, Firefox, Edge, etc.)
- Não é necessário instalar dependências ou servidores adicionais
