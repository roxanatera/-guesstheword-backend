from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Lista de palabras para el juego
PALABRAS = ["python", "javascript", "react", "flask", "programacion", "frontend"]

# Variables globales
palabra_secreta = random.choice(PALABRAS)
letras_adivinadas = []
intentos_restantes = 6

@app.route("/", methods=["GET"])
def home():
    return "Servidor del Ahorcado funcionando correctamente", 200

@app.route("/reset", methods=["POST"])
def reset_game():
    global palabra_secreta, letras_adivinadas, intentos_restantes
    palabra_secreta = random.choice(PALABRAS)
    letras_adivinadas = []
    intentos_restantes = 6
    return jsonify({"message": "Juego reiniciado"}), 200

@app.route("/guess", methods=["POST"])
def guess_letter():
    global letras_adivinadas, intentos_restantes
    data = request.get_json()
    letra = data.get("letter")

    if not letra or len(letra) != 1:
        return jsonify({"message": "Debes enviar una letra válida"}), 400

    letra = letra.lower()
    if letra in letras_adivinadas:
        return jsonify({"message": "Letra ya adivinada", "status": "repetida", "used_letters": letras_adivinadas}), 200

    letras_adivinadas.append(letra)

    if letra not in palabra_secreta:
        intentos_restantes -= 1

    progreso = "".join([l if l in letras_adivinadas else "_" for l in palabra_secreta])

    if "_" not in progreso:
        return jsonify({"status": "ganaste", "progress": progreso, "used_letters": letras_adivinadas}), 200
    elif intentos_restantes <= 0:
        return jsonify({
            "status": "perdiste",
            "progress": progreso,
            "correct_word": palabra_secreta,
            "used_letters": letras_adivinadas
        }), 200

    return jsonify({
        "status": "jugando",
        "progress": progreso,
        "attempts_left": intentos_restantes,
        "used_letters": letras_adivinadas
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
