from flask import Flask, request, jsonify, send_from_directory
import os
import json
import time

app = Flask(__name__)

UPLOAD_FOLDER = "files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return "APK Sync Server Running"


@app.route("/upload", methods=["POST"])
def upload():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        # Si el JSON trae nombre de archivo usarlo
        filename = data.get("filename")

        # Si no trae filename usar nombre automático
        if not filename:
            filename = f"sync_{int(time.time())}.json"

        filepath = os.path.join(UPLOAD_FOLDER, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return jsonify({
            "status": "saved",
            "file": filename
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route("/files", methods=["GET"])
def list_files():
    try:
        files = os.listdir(UPLOAD_FOLDER)
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/delete/<filename>", methods=["DELETE"])
def delete_file(filename):
    try:
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        if os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({"status": "deleted", "file": filename})
        else:
            return jsonify({"error": "file not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
