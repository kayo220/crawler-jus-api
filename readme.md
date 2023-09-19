
# Crawler-API

API criada em python (v.3.11.5) para expor consultas relacionadas à processos jurídicos. 

Sites para busca: 

    - TJAL
        - 1º grau - https://www2.tjal.jus.br/cpopg/open.do
        - 2º grau - https://www2.tjal.jus.br/cposg5/open.do
    - TJCE
        - 1º grau - https://esaj.tjce.jus.br/cpopg/open.do
        - 2º grau - https://esaj.tjce.jus.br/cposg5/open.do

API hospedada na AWS através do EC2 (desativada em 19/09/2023 - AWS free tier): [52.55.52.3](http://54.233.75.213/)

# Passo a passo (com docker):
- docker-compose up (no diretório raiz do projeto)
    - rota: localhost:5000

# Passo a passo (sem docker):
- Instalação das dependências: 
    - pip3 install scrapy
    - pip3 install flask
    - pip3 install flask_restx
    - pip3 install pytest
    - pip3 install python-dotenv
- Execução da API (no diretório raiz do projeto)
    - flask run
    - rota: localhost:5000
- Execução dos testes (no diretório raiz do projeto)
    - pytest
