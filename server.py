import requests
from flask import Flask, jsonify
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

@app.route('/seguidores/<usuario>', methods=['GET'])
def obtener_seguidores(usuario):
    url = f'https://www.instagram.com/{usuario}/'

    # Realizar la solicitud HTTP a Instagram
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Intentar extraer el número de seguidores desde el JavaScript incrustado
        try:
            # Buscar un script que contiene los datos
            script_tag = soup.find('script', text=lambda t: t.startswith('window._sharedData'))
            
            # Extraer el JSON del script
            shared_data = script_tag.string.split(' = ', 1)[1].rstrip(';')
            data = json.loads(shared_data)
            
            # Obtener la cantidad de seguidores
            followers = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_followed_by']['count']
            return jsonify({'seguidores': followers})

        except Exception as e:
            return jsonify({'error': f'No se pudo obtener los datos de seguidores. Error: {str(e)}'})
    else:
        return jsonify({'error': 'Error al acceder a la página de Instagram'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
