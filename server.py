from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"mensaje": "Servidor de Seguidores Instagram funcionando correctamente 🚀"})

@app.route('/seguidores/<usuario>')
def seguidores(usuario):
    try:
        url = f"https://www.instagram.com/{usuario}/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return jsonify({"error": f"No se pudo acceder a la página de Instagram. Status code: {response.status_code}"}), 500

        soup = BeautifulSoup(response.text, 'html.parser')

        description = soup.find("meta", attrs={"name": "description"})
        
        if not description:
            return jsonify({"error": "No se encontró la descripción del perfil."}), 500

        content = description.get("content", "")
        match = re.search(r"([\d,.]+) Followers", content)

        if not match:
            return jsonify({"error": "No se pudo encontrar el número de seguidores."}), 500

        followers_text = match.group(1).replace(",", "").replace(".", "")
        followers = int(followers_text)

        return jsonify({"seguidores": followers})

    except Exception as e:
        return jsonify({"error": f"Excepción capturada: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
