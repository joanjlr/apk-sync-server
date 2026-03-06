from flask import Flask, request, jsonify
import os

app = Flask(__name__)

DATA_FOLDER = "data"

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

@app.route("/")
def home():
    return "Servidor APK Sync funcionando"

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    filepath = os.path.join(DATA_FOLDER, file.filename)
    file.save(filepath)
    return jsonify({"status": "ok"})

@app.route("/files", methods=["GET"])
def files():
    return jsonify(os.listdir(DATA_FOLDER))

@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    from flask import send_from_directory
    return send_from_directory(DATA_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
