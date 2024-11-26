from flask import Flask, request, send_from_directory, jsonify
import os

app = Flask(__name__)
FILE_DIRECTORY = "files"

if not os.path.exists(FILE_DIRECTORY):
    os.makedirs(FILE_DIRECTORY)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    file.save(os.path.join(FILE_DIRECTORY, file.filename))
    return jsonify({"message": "File uploaded successfully"}), 200

@app.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    try:
        return send_from_directory(FILE_DIRECTORY, filename)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

@app.route('/files', methods=['GET'])
def list_files():
    try:
        files = os.listdir(FILE_DIRECTORY)
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
