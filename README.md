# DPC Example Frontend (Flask)

This project demonstrates how an application might interact with the DPC application to retrieve medicare data.

For more information about DPC, see https://github.com/CMSgov/dpc-app

## Setup

For setup, it's recommended to create a dedicated python3 virtual environment like so:

```bash
git clone https://github.com/isears/dpc-flask-example/
cd dpc-flask-example/
python3 -m venv venv
pip install -r requirements.txt
```

## Run

Run within the same venv that was created during setup.
```bash
export FLASK_APP=main.py
python -m flask run
```