# Products API

## Descrição:
Web Api de produtos com suporte á criação e autenticação de usuários para acesso de rotas administrativas (CREATE, UPDATE, DELETE) de produtos.

## Autenticação
Algumas rotas requerem autenticação via token (obtido no endpoint de login) no cabeçalho (header) da requisição. 

Os tokens são hashs sha256 e possuem expiração de 5 min. Então será necessário logar novamente para ativá-lo novamente

- Example Request Header
Key: token
Value: "09e98f54d3e5c63e9d6920639466c6db5408f0bea335f3a8919606fd09f368e3"

Caso token não fornecido em endpoints que requerem autenticação, messagem abaixo será recebida:

[401] - Unauthorized
```json
{
    "message": "Not Authorized!"
}
```

## Rotas (Endpoints)
### Health Check
#### [GET] /health_check
**Descrição:** Endpoint para saber a saúde do servidor

Caso retorne status code 200, está saudável
Caso retorne qualquer outro status code, está com algum problema

### Users
#### [POST] /register 
**Descrição:** Endpoint para criação de usuários

- Request Body (JSON)
```json
{
    "username": "fulano",
    "password": "senha123"    
}
```

Quando o usuário foi inserido com sucesso:
- Response [201] - Created
```json
{
    "message": "User was been insert sucessfully!",
    "status_code": 201
}
```

Quando o usuário já existe com sucesso:
- Response [400] - Bad Request
```json
{
    "message": "User Already Exists!",
    "status_code": 400
}
```

Quando houve problema nos dados da requisição:
- Response [400] - Bad Request
```json
{
    "message": "Username and password are required! | Username and password must be text | password must have between 6 and 8 characters!",
    "status_code": 400
}
```

Detalhe importante: Como medida de segurança, as senhas "cruas" não são armazenadas no banco de dados, e sim o seu hash.

#### [POST] /login 
**Descrição:** Endpoint para obtenção e/ou ativação do token

- Request Body (JSON)
```json
{
    "username": "fulano",
    "password": "senha123"    
}
```

Quando o usuário foi encontrado com sucesso:
- Response [200] - Ok
```json
{
    "data": {
        "token": "09e98f54d3e5c63e9d6920639466c6db5408f0bea335f3a8919606fd09f368e3",
        "token_activate_at": "Sun, 13 Oct 2024 18:24:48 GMT"
    },
    "message": "User is Logged!",
    "status_code": 200
}
```
OBS: O horário de expiração do token vai ser baseado no horário do servidor, ou seja, pode ter diferenças no fuso horário. Todavia, isso não vai impactar no tempo de duração do token.

Quando o usuário não foi encontrado com sucesso:
- Response [400] - Bad Request
```json
{
    "error": {},
    "message": "User not Found!",
    "status_code": 400
}
```

Quando houve problema nos dados da requisição:
- Response [400] - Bad Request
```json
{
    "message": "Username and password are required! | Username and password must be text | password must have between 6 and 8 characters!",
    "status_code": 400
}
```

### Products
#### [GET] /api/products 
**Descrição:** Endpoint para obtenção de todos os produtos salvos

Quando algum produto foi encontrado:
- Response [200] - Ok
```json
{
    "data": [
        {
            "id": 1,
            "name": "nomeProduto",
            "unit_price": 10,
            "quantity": 5
        }
    ],
    "status_code": 200
}
```

Quando nenhum produto foi encontrado:
- Response [400] - Bad Request
```json
{
    "error": {},
    "message": "Product has not Found!",
    "status_code": 400
}
```

#### [GET] /api/products/<id> 
**Descrição:** Endpoint para obtenção de um produto salvo pelo id

Quando algum produto foi encontrado:
- Response [200] - Ok
```json
{
    "data": {
            "id": 1,
            "name": "nomeProduto",
            "unit_price": 10,
            "quantity": 5
        },
    "status_code": 200
}
```

Quando o produto não foi encontrado:
- Response [400] - Bad Request
```json
{
    "message": "Product not Found!"
}
```
Quando houve problema nos dados da requisição:
- Response [400] - Bad Request
```json
{
    "message": "id must be numeric!",
    "status_code": 400
}
```


#### [POST] /api/products (**Authentication required**)
**Descrição:** Endpoint para criação de um produto

- Request Body (JSON)
```json
{
    "name": "nomeProduto",
    "unit_price": 14,
    "quantity": 3
}
```

Quando o produto foi inserido com sucesso:
- Response [200] - Ok
```json
{ 
    "message": "Product has been inserted!", 
    "status_code": 200 
}
```

Quando o produto não foi inserido com sucesso:
- Response [400] - Bad Request
```json
{ 
    "message": "Product has not been inserted!", 
    "error": "Erro qualquer", 
    "status_code": 400 
}
```
Quando houve problema nos dados da requisição:
- Response [400] - Bad Request
```json
{
    "message": "name, unit_price and quantity are required! | name, unit_price and quantity must be respectively text, decimal and numeric! | name must be have at least 20 characters long!",
    "status_code": 400
}
```

#### [PUT] /api/products/<id> (**Authentication required**)
**Descrição:** Endpoint para alteração de um produto

- Request Body (JSON)
```json
{
    "name": "novoNomeProduto",
    "unit_price": 14,
    "quantity": 3
}
```

Quando o produto foi atualizado com sucesso:
- Response [200] - Ok
```json
{
    "message": "Product has been updated sucessfuly!", 
    "status_code" : 200
}
```

Quando o produto não foi atualizado com sucesso:
- Response [400] - Ok
```json
{
    "message": "Product has been not updated sucessfuly!", 
    "status_code" : 400,
    "error": "Um erro qualquer"
}
```

Quando o produto não foi encontrado no banco de dados:
- Response [404] - Not Found
```json
{ 
    "message": "Product has not Found!", 
    "status_code": 404 
}
```
Quando houve problema nos dados da requisição:
- Response [400] - Bad Request
```json
{
    "message": "name, unit_price and quantity are required! | name, unit_price and quantity must be respectively text, decimal and numeric! | name must be have at least 20 characters long!",
    "status_code": 400
}
```


#### [DELETE] /api/products/<id> (**Authentication required**)
**Descrição:** Endpoint para remoção de um produto

Quando o produto foi removido com sucesso:
- Response [204] - No Content
```json
{}
```

Quando o produto não foi removido com sucesso:
- Response [400] - Bad Request
```json
{
    "message": "Product has been not deleted sucessfuly!", 
    "status_code" : 400,
    "error": "Um erro qualquer"
}
```

Quando o produto não foi encontrado no banco de dados:
- Response [404] - Not Found
```json
{
    "message": "Product has not Found!", 
    "status_code": 404
}
```

Quando houve problema nos dados da requisição:
- Response [400] - Bad Request
```json
{
    "message": "id must be numeric!",
    "status_code": 400
}
```

## Configuração e Execução

### Requisitos
- Docker
- Docker Compose
- Git
(Se você usar windows, o software Docker Desktop já instale o docker e o docker compose)

### Execução 
Após instalar todas as dependências acima, segue os passos para executar o projeto:

1. Clonar repositório
2. Abrir pasta do repositório
3. Rodar o comando docker-compose up --build

E pronto! Agora é só testar a API usando a porta `80` do seu host, usando o ip publico ou dns.
(Ex: Localhost -> `http://localhost` ou `http://127.0.0.1`
     AWS EC2   -> `http://123.123.123.123` (IP publico))

## Configuração completa em um EC2 AWS
### 1. 