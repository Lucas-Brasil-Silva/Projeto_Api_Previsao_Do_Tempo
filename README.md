# Projeto_Api_Previsao_Do_Tempo
<p align="justify">Este projeto abrangente engloba a obtenção de dados climáticos, armazenamento desses dados e uma API de previsão do tempo que fornece acesso a informações climáticas atualizadas. Além disso, inclui recursos de controle de solicitações para garantir o uso adequado da API. O objetivo do desenvolvimento deste projeto é solidificar os conhecimentos em desenvolvimento de APIs.</p>

## 🔗 Recursos e Objetivos
-  Obtenção de dados climáticos do **[INMET: Instituto Nacional de Meteorologia](https://portal.inmet.gov.br/)**, atualizados periodicamente.
- Armazenamento de dados climáticos em um banco de dados.
- API de previsão do tempo que fornece acesso aos dados armazenados.
- Controle de solicitações para proteger contra uso excessivo.

## 🛠️ Tecnologias Utilizadas
Principais tecnologias usadas:
[Flask](https://readthedocs.org/projects/flask/) - [Flask-Limiter](https://readthedocs.org/projects/flask/) -
[SQLAlchemy](https://readthedocs.org/projects/flask/) - [Pymongo](https://readthedocs.org/projects/flask/) - 
 [Selenuim](https://readthedocs.org/projects/flask/) -
[Scrapy](https://readthedocs.org/projects/flask/) entre outras.

## 📌 Status do Projeto
<h4 align="center"> 
	✅ Projeto concluído para fins educacionais ✅ 
</h4>


## 🔧 Instruções de Uso

### 📋 Instalação Das Dependências
Para instalar as dependências do projeto, execute o seguinte comando:
```bash
pip install -r requirements.txt
```
### ⚙️ Iniciar a Spider de Obtenção de Dados
Para iniciar a spider que obtém os dados climáticos, execute o seguinte comando:
```bash
python executando_spider.py
```

### ⚙️ Iniciar a API de Previsão do Tempo
Para iniciar a API de previsão do tempo, execute o seguinte comando:
```bash
Python api_clima.py
```
## 🚀 Primeiro Acesso à API Previsão do Tempo
Para realizar o primeiro acesso à API de Previsão do Tempo, siga as instruções abaixo:

### Formulário de Registro
_____
*Exemplo de Requisição:*

```python
import requests

reposta_formulario = requests.get('http://localhost:5000/cadastro/formulario')
print(reposta_formulario.json())
```
*Resposta Esperada:*
```json
{'email': 'Seu email',
 'nome': 'Seu nome',
 'senha': 'Sua senha'}
```
### Registro de novos usuários:
____
*Exemplo de Requisição:*
```python
formulario = {'email': 'davibrasil@gmail.com',
            'nome': 'davi',
            'senha': 'davi123'}

resposta_cadastro = requests.post('http://localhost:5000/cadastro',json=formulario)
print(resposta_cadastro.json()) 
```
*Resposta Esperada:*
```json
{'mensagem': 'Cadastro realizado com sucesso!'}
```

### Autenticação de login e gereção de chave API:
____
*Exemplo de Requisição:*
```python
resposta_login = requests.get('http://localhost:5000/login',auth=('davi','davi123'))
print(resposta_login.json())
```
*Resposta Esperada:*
```json
{'x-api-key':'47ec8bad-27ef-4b2b-89ea-34eb8dbd4087'}
```

### Previsão do tempo para Florianópolis:
______
*Exemplo de Requisição:*
```python
resposta_tempo = requests.get('http://localhost:5000/tempo',headers={'x-api-key':'47ec8bad-27ef-4b2b-89ea-34eb8dbd4087'})
print(resposta_tempo.json())
```
*Resposta Esperada:*
```json
{'cidade': 'Florianópolis',
    'codicao meteorologica': ' Muitas nuvens com chuva isolada ',
    'data': ' 13/09/2023 - Quarta',
    'temperatura': '22°C', 
    'umidade': '75%', 
    'vento': 'Fracos'}
```

### Previsão do tempo para cidade específica:
____
*Exemplo de Requisição:*
```python
resposta_cidade = requests.get('http://localhost:5000/tempo/cidade/São Paulo',headers={'x-api-key':'47ec8bad-27ef-4b2b-89ea-34eb8dbd4087'})
print(resposta_cidade.json())
```
*Resposta Esperada:*
``` json
{'cidade': 'São Paulo', 
    'codicao meteorologica': ' Poucas nuvens ', 
    'data': ' 13/09/2023 - Quarta',
    'temperatura': '26°C', 
    'umidade': '42%', 
    'vento': 'Moderados com rajadas'}
```

### Previsão do tempo para cidade específica ao longo da semana:
___
*Exemplo de Requisição:*
```python
resposta_cidade_semana = requests.get('http://localhost:5000/tempo/cidade/São Paulo/semana',headers={'x-api-key':'47ec8bad-27ef-4b2b-89ea-34eb8dbd4087'})
print(resposta_cidade_semana.json())
```
*Resposta Esperada:*
``` Json
[{'cidade': 'São Paulo', 
    'codicao meteorologica': ' Poucas nuvens ', 
    'data': ' 13/09/2023 - Quarta', 
    'temperatura': '26°C', 
    'umidade': '42 % ', 
    'vento': 'Moderados com rajadas'},

    {'cidade': 'São Paulo', 
    'codicao meteorologica': ' Muitas nuvens com pancadas de chuva e trovoadas isoladas ', 
    'data': ' 14/09/2023 - Quinta', 
    'temperatura': '18°C', 
    'umidade':'62%', 
    'vento': 'Moderados com rajadas'}, 

    {'cidade': 'São Paulo', 
    'codicao meteorologica': ' Muitas nuvens com chuva isolada ', 
    'data': ' 15/09/2023 - Sexta', 
    'temperatura': '15°C', 
    'umidade': '70%', 
    'vento': 'Moderados'}, 

    {'cidade': 'São Paulo', 
    'codicao meteorologica': ' Muitas nuvens com nevoeiro ', 
    'data': ' 16/09/2023 - Sábado', 
    'temperatura': '20°C', 
    'umidade': '67%', 
    'vento': 'Fraco/Moderado'}, 

    {'cidade': 'São Paulo', 
    'codicao meteorologica': ' Poucas nuvens ', 
    'data': ' 17/09/2023 - Domingo', 
    'temperatura': '24°C', 
    'umidade': '60%', 
    'vento': 'Fraco/Moderado'}]
```
___
