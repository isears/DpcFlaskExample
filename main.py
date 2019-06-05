from flask import Flask
from flask import render_template
from flask import request
from flask import g
from util import *

import json
import sqlite3


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
DATA_FETCHER = DPCDataFetcher('8D80925A-027E-43DD-8AED-9A501CC4CD91')
DATA_DISPLAY_LIMIT = 10


@app.route('/')
def main_menu():
    return render_template('index.html')


@app.route('/api/getdata')
def get_data():
    print('packaging data for frontend')
    return render_template('table.html', beneficiaries=DATA_FETCHER.in_memory_datastore[0:DATA_DISPLAY_LIMIT])


@app.route('/api/check_status')
def check_status():
    state = DATA_FETCHER.update_state()
    print(state)
    return json.dumps(state)


@app.route('/api/refresh_data')
def refresh_data():
    print('Refreshing data...')
    DATA_FETCHER.start_request()
    return '', 202

