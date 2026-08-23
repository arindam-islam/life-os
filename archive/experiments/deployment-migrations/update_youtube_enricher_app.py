import subprocess

app_code = '''import json
import urllib.request
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/enrich', methods=['POST'])
def enrich():
    data = request.get_json() or {}
    url = data.get('url', '')
    if not url:
        return jsonify({'ok': False, 'error': 'Missing url'}), 400

    try:
        payload = json.dumps({'url': url}).encode('utf-8')
        req = urllib.request.Request(
            'http://172.17.0.1:8089/process',
            data=payload,
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=45) as resp:
            res_json = json.loads(resp.read().decode('utf-8'))
            return jsonify({
                'ok': True,
                'video': {
                    'title': res_json.get('topic', 'Captured Resource'),
                    'description': res_json.get('story', ''),
                    'uploader': ''
                },
                'analysis': res_json
            })
    except Exception as e:
        return jsonify({
            'ok': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
'''

with open('/tmp/youtube_enricher_app.py', 'w') as f:
    f.write(app_code)

print("✅ Updated youtube-enricher app.py with 45s timeout!")
