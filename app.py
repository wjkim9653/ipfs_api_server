from flask import Flask, request, jsonify, send_file
import requests
import tempfile
import os

app = Flask(__name__)

IPFS_API_URL = os.environ.get("IPFS_API_URL", "http://127.0.0.1:5001/api/v0")
API_KEY = os.environ.get("API_KEY", "mysecretkey")

@app.before_request
def auth():
    if request.headers.get("X-API-KEY") != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

@app.route("/upload", methods=["POST"])
def upload_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No PDF file provided"}), 400

    file = request.files["file"]

    if not file.filename.endswith(".pdf"):
        return jsonify({"error": "Only PDF files allowed"}), 400

    files = {"file": (file.filename, file.stream, "application/pdf")}

    try:
        res = requests.post(f"{IPFS_API_URL}/add", files=files)
        res.raise_for_status()
        return jsonify({"cid": res.json()["Hash"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download", methods=["POST"])
def download_pdf():
    data = request.get_json()
    cid = data.get("cid")

    if not cid:
        return jsonify({"error": "CID is required"}), 400

    try:
        res = requests.post(f"{IPFS_API_URL}/cat?arg={cid}", stream=True)
        res.raise_for_status()

        # PDF 파일로 저장
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        for chunk in res.iter_content(8192):
            tmp.write(chunk)
        tmp.close()

        return send_file(tmp.name, as_attachment=True, download_name=f"{cid}.pdf", mimetype="application/pdf")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
