import http.client
from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Servidor en funcionamiento ✅✅✅"

@app.route('/seguidores/<usuario>', methods=['GET'])
def obtener_seguidores(usuario):
    try:
        # Establecemos la conexión con la API
        conn = http.client.HTTPSConnection("instagram230.p.rapidapi.com")

        headers = {
            'x-rapidapi-key': "7526c9822dmsh930262a907292e3p14e474jsn9031726bd6df",  # Tu clave API aquí
            'x-rapidapi-host': "instagram230.p.rapidapi.com"
        }

        # Hacemos la solicitud GET a la API de RapidAPI para obtener los detalles del usuario
        conn.request("GET", f"/user/details?username={usuario}", headers=headers)

        # Obtenemos la respuesta
        res = conn.getresponse()
        data = res.read()

        # Decodificamos la respuesta
        json_data = json.loads(data.decode("utf-8"))

        # Verificamos si la respuesta contiene los seguidores
        if 'data' in json_data and 'user' in json_data['data']:
            followers_count = json_data['data']['user'].get('edge_followed_by', {}).get('count', None)
            if followers_count is not None:
                return jsonify({"seguidores": followers_count})
            else:
                return jsonify({"error": "No se pudo obtener el número de seguidores."})
        else:
            return jsonify({"error": "Respuesta inesperada de la API."})

    except Exception as e:
        return jsonify({"error": f"No se pudo obtener los datos. Error: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

#if __name__ == '__main__':
#    app.run(debug=True)



