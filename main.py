from flask import Flask
from flask import render_template
from flask import request
from flask import g
from util import *

import json
import sqlite3


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
# TODO: Handle "Last DPC request failed" condition
BACKEND_STATE = {
    'active': False,
    'provider_id': '8D80925A-027E-43DD-8AED-9A501CC4CD91'
}
DATA_FETCHER = DPCDataFetcher(BACKEND_STATE['provider_id'])
DATA_DISPLAY_LIMIT = 10


@app.route('/')
def main_menu():
    return render_template('index.html')


@app.route('/api/getdata')
def get_data():
    print('packaging data for frontend')

    return render_template('table.html', beneficiaries=DATA_FETCHER.in_memory_datastore[0:DATA_DISPLAY_LIMIT])
    #return json.dumps(DATA_FETCHER.in_memory_datastore[0:DATA_DISPLAY_LIMIT])


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


# Recommendation found in flask documentation
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = sqlite3.connect(DATABASE)
    return db


# Recommendation found in flask documentation
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


