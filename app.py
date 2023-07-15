from flask import Flask, request, jsonify, render_template
import subprocess
import shlex

app = Flask(__name__)

api_key = ''

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    url = shlex.quote(request.form['url'])
    command = f'python3 gepetto.py --api={api_key} gepetto scan {url} | jq .'
    result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
    return jsonify(result=result.stdout)

@app.route('/report', methods=['POST'])
def report():
    url_hash = shlex.quote(request.form['url_hash'])
    command = f'python3 gepetto.py --api={api_key} gepetto report {url_hash} | jq .'
    result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
    return jsonify(result=result.stdout)

@app.route('/screenshot', methods=['POST'])
def screenshot():
    url_hash = shlex.quote(request.form['url_hash'])
    command = f'python3 gepetto.py --api={api_key} gepetto screenshot {url_hash}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
    if "Successfully wrote to " in result.stdout:
        filename = result.stdout.split("Successfully wrote to ")[1].strip()
        open_command = f'open {filename}'
        open_result = subprocess.run(open_command, shell=True, capture_output=True, text=True, check=True)
    return jsonify(result=result.stdout)

if __name__ == '__main__':
    app.run(debug=True)
