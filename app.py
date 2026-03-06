from flask import Flask, request, jsonify, send_from_directory
import os
import json
import time

app = Flask(__name__)

UPLOAD_FOLDER = "files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/upload", methods=["POST"])
def upload():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        filename = f"sync_{int(time.time())}.json"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f)

        return jsonify({"status": "saved", "file": filename})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/files", methods=["GET"])
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify(files)


@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/")
def home():
    return "APK Sync Server Running"


if __name__ == "__main__":
    app.run()
