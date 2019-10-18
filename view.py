from app import app
from flask import render_template
from flask import request
from flask import jsonify
import uuid
import model


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    email = request.args.get('email')
    print(email)
    url = request.args.get('url')
    print(url)

    id = uuid.uuid4()

    model.Task(str(id), url, email).run()

    return jsonify({'id': str(id)}), 200

@app.route('/check')
def check():
    id = request.args.get('id')
    results = model.check(id)
    if results['status'] == 'done':
        return jsonify(results), 200
    elif results['status'] == 'running':
        return jsonify({'status': 'running'}), 102
    elif results['status'] == 'does not exist':
        return jsonify({'status': 'does not exist'}), 404
    else:
        return jsonify({'status': 'error'}), 500
