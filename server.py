import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Datos de tu API
RAPIDAPI_HOST = "instagram230.p.rapidapi.com"
RAPIDAPI_KEY = "7526c9822dmsh930262a907292e3p14e474jsn9031726bd6df"

@app.route('/')
def home():
    return "Servidor en funcionamiento ✅"

@app.route('/seguidores/<usuario>', methods=['GET'])
def obtener_seguidores(usuario):
    url = f"https://{RAPIDAPI_HOST}/user/details"
    querystring = {"username": usuario}
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        # ⚠️ Ajustamos a la estructura real de la respuesta JSON
        seguidores = data["data"]["edge_followed_by"]["count"]

        return jsonify({"seguidores": seguidores})

    except Exception as e:
        return jsonify({"error": f"No se pudo obtener los seguidores. Error: {str(e)}"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
