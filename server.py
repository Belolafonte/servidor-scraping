from flask import Flask, jsonify
import requests
import re   

app = Flask(__name__)


@app.route('/')
def home():
    return "¡El servidor está funcionando!"
    
def get_instagram_followers(username):
    url = f"https://www.instagram.com/{username}/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None

    match = re.search(r'"edge_followed_by":{"count":(\d+)}', response.text)
    if match:
        return int(match.group(1))
    else:
        return None

@app.route('/seguidores/<username>', methods=['GET'])
def seguidores(username):
    followers = get_instagram_followers(username)
    if followers is None:
        return jsonify({"error": "No se pudo obtener el número de seguidores"}), 500
    return jsonify({"followers": followers})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
