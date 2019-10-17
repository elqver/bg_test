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

    for i in request.args:
        print(i, request.args[i])

    email = request.args.get('email')
    print(email)
    url = request.args.get('url')
    print(url)

    id = uuid.uuid4()

    model.Task(str(id), url, email).run()

    return jsonify({'id': str(id)}), 200
