# Código em Python que vai até a rota http://127.0.0.1:5000/product/json/ e imprime o JSON retornado.
import requests as request
import json

url = 'http://127.0.0.1:5000/product/json'

response = request.get(url)
print(json.dumps(response.json(), indent=4))