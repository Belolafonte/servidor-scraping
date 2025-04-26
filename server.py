from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

@app.route('/')
def home():
    return "¡El servidor está funcionando!"

@app.route('/seguidores/<usuario>', methods=['GET'])
def obtener_seguidores(usuario):
    url = f'https://www.instagram.com/{usuario}/'

    # Realizar la solicitud HTTP a Instagram
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscar el número de seguidores
        script_tag = soup.find('script', text=lambda t: t.startswith('window._sharedData'))
        
        if script_tag:
            shared_data = script_tag.string.split(' = ', 1)[1].rstrip(';')
            data = json.loads(shared_data)
            followers = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_followed_by']['count']
            return jsonify({'seguidores': followers})
        else:
            return jsonify({'error': 'No se pudo obtener los datos de seguidores'})
    else:
        return jsonify({'error': 'Error al acceder a la página de Instagram'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

