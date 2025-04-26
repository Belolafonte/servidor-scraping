import instaloader
from flask import Flask, jsonify

app = Flask(__name__)

# Inicializamos instaloader
L = instaloader.Instaloader()

@app.route('/seguidores/<usuario>', methods=['GET'])
def obtener_seguidores(usuario):
    try:
        # Cargar la cuenta de Instagram
        profile = instaloader.Profile.from_username(L.context, usuario)

        # Obtener el número de seguidores
        followers = profile.followers
        return jsonify({'seguidores': followers})

    except instaloader.exceptions.InstaloaderException as e:
        return jsonify({'error': f'No se pudo obtener los datos de seguidores. Error: {str(e)}'})

if __name__ == '__main__':
    # Mensaje de inicio para confirmar que el servidor está corriendo
    print("Servidor iniciado correctamente en http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000)
