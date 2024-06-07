import requests

response = requests.get('https://www.google.com')
print(f"Status Code: {response.status_code}")
print(f"Content: {response.text[:100]}")  # Imprime los primeros 100 caracteres del contenido
