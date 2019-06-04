from flask import Flask
from flask import render_template
from flask import request
from util import *

import json


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
BACKEND_STATE = {
    'active': False,
    'provider_id': "8D80925A-027E-43DD-8AED-9A501CC4CD91"
}
DATA_FETCHER = DPCDataFetcher(BACKEND_STATE['provider_id'])

@app.route('/')
def main_menu():
    return render_template('index.html')


@app.route('/api/check_status')
def check_status():
    if DATA_FETCHER.isDone():
        BACKEND_STATE['active'] = False
        
    return json.dumps(BACKEND_STATE)


@app.route('/api/refresh_data')
def refresh_data():
    print('Refreshing data...')
    BACKEND_STATE['active'] = True
    DATA_FETCHER.start_request()
    return '', 202



