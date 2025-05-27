from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# 设置上传文件的目录
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return "Welcome to the file upload server!"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    # 直接保存文件，不做任何类型检查
    filename = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filename)
    return jsonify({'message': 'File uploaded successfully', 'filename': file.filename}), 200

if __name__ == '__main__':
    # 启动 HTTPS 服务器
    #app.run(ssl_context=('server.crt', 'server.key'), host='0.0.0.0', port=444)
    app.run(host='0.0.0.0', port=444)
