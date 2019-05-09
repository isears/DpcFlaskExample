from flask import Flask
from flask import render_template
from flask import request
from util import *

app = Flask(__name__)


@app.route('/')
def main_menu():
    return render_template('index.html')


@app.route('/make_request', methods=['GET'])
def make_request():
    return render_template('request.html')


@app.route('/make_request', methods=['POST'])
def handle_make_request():
    dpc_request(request.form['provider_id'])

    return render_template(
        'request.html',
        provider_id=request.form['provider_id']
    )


@app.route('/view_requests')
def view_requests():
    return render_template('view.html')



