import requests
import json

# URL del servicio
url = 'http://localhost:5001/api/jedi'

# Recordemos que estamos enviando los datos en formato JSON
# De esta forma es más fácil convertirlo a String posteriormente
datos = {
    'id': 5,
    'name': 'Ashoka',
}

# Convertimos el diccionario a String
json_data = json.dumps(datos)

# Indicamos que enviaremos contenido JSON
headers = {'Content-Type': 'application/json'}

# POST request
response = requests.post(url, data=json_data, headers=headers)

# ¿Éxito?
if response.status_code == 200:
    # Procesar la respuesta
    print(response.json())
else:
    # Procesar el error
    print(f"Error: {response.status_code} - {response.text}")
