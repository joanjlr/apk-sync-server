from flask import Flask, request, jsonify, send_from_directory
import os
import json
import time

app = Flask(__name__)

CARPETA_ARCHIVOS = "files"
os.makedirs(CARPETA_ARCHIVOS, exist_ok=True)


@app.route("/")
def inicio():
    return "Servidor de sincronización APK funcionando"


@app.route("/upload", methods=["POST"])
def subir_archivo():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No se recibió JSON"}), 400

        tipo = data.get("tipo_envio", "")

        # Determinar nombre según tipo
        if tipo == "FULL_SYNC":
            filename = f"sync_{int(time.time())}.json"

        elif tipo == "CATALOGO_PRODUCTOS":
            filename = "lista_productos.json"

        elif tipo == "AVANCE":
            filename = "avance_dependiente.json"

        elif tipo == "ENVIO_DIA":
            filename = "cierre_dia_dependiente.json"

        else:
            filename = f"sync_{int(time.time())}.json"

        filename = os.path.basename(filename)

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

    filename = os.path.basename(filename)
    ruta = os.path.join(CARPETA_ARCHIVOS, filename)

    if not os.path.exists(ruta):
        return jsonify({"error": "archivo no encontrado"}), 404

    return send_from_directory(CARPETA_ARCHIVOS, filename)


@app.route("/delete/<filename>", methods=["DELETE"])
def eliminar_archivo(filename):

    filename = os.path.basename(filename)
    ruta = os.path.join(CARPETA_ARCHIVOS, filename)

    if os.path.exists(ruta):
        os.remove(ruta)
        return jsonify({
            "estado": "archivo eliminado",
            "archivo": filename
        })
    else:
        return jsonify({"error": "archivo no encontrado"}), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)