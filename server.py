import http.client
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
      return "Servidor en funcionamiento ✅"

@app.route('/seguidores/<usuario>', methods=['GET'])
def obtener_seguidores(usuario):
    try:
        conn = http.client.HTTPSConnection("instagram230.p.rapidapi.com")

        headers = {
            'x-rapidapi-key': "TU_RAPIDAPI_KEY",
            'x-rapidapi-host': "instagram230.p.rapidapi.com"
        }

        # Realizamos la petición para obtener los detalles del usuario
        conn.request("GET", f"/user/details?username={usuario}", headers=headers)

        res = conn.getresponse()
        data = res.read()
        json_data = data.decode("utf-8")

        # Cargamos el JSON y extraemos el número de seguidores
        import json
        data_parsed = json.loads(json_data)

        if 'data' in data_parsed:
            seguidores = data_parsed['data']['user']['edge_followed_by']['count']
            return jsonify({'seguidores': seguidores})
        else:
            return jsonify({'error': 'No se pudo obtener los datos de seguidores'})

    except Exception as e:
        return jsonify({'error': f'Error al obtener datos: {str(e)}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
