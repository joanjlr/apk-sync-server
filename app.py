from flask import Flask, request, jsonify, send_from_directory
import os
import json

app = Flask(__name__)

CARPETA_ARCHIVOS = "files"
os.makedirs(CARPETA_ARCHIVOS, exist_ok=True)


@app.route("/")
def inicio():
    return "Servidor funcionando"


@app.route("/upload", methods=["POST"])
def subir_archivo():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No se recibió JSON"}), 400

        # Siempre guardar con el mismo nombre
        filename = "archivo_recibido.json"

        ruta = os.path.join(CARPETA_ARCHIVOS, filename)

        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return jsonify({
            "estado": "guardado",
            "archivo": filename
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/files", methods=["GET"])
def listar_archivos():
    try:
        archivos = os.listdir(CARPETA_ARCHIVOS)
        return jsonify(archivos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/download/<filename>", methods=["GET"])
def descargar_archivo(filename):

    ruta = os.path.join(CARPETA_ARCHIVOS, filename)

    if not os.path.exists(ruta):
        return jsonify({"error": "archivo no encontrado"}), 404

    return send_from_directory(CARPETA_ARCHIVOS, filename)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)