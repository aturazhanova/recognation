from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/proxy/extract_text', methods=['POST'])
def proxy_extract_text():
    target_url = 'http://127.0.0.1:5000/extract_text'
    resp = requests.post(target_url, json=request.get_json())
    return (resp.content, resp.status_code, resp.headers.items())

if __name__ == '__main__':
    app.run(port=5001)
