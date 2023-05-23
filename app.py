# Add this to app.py
from flask import Flask
from flask import request
import requests
from get_database_connection import get_database_connection
from datetime import datetime
from services.aws.get_drones_data_by_date_range import get_drones_data_by_date_range
from services.aws.save_drones_report import save_drones_report
from services.reports.generate_drones_report import generate_drones_json_report
from util.is_datetime_iso_valid import is_datetime_iso_valid

from dotenv import load_dotenv
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/hw')
def hello_world2():
    return 'Hello World 222!'


@app.get('/report_pg')
def report_pg():

    start_date = request.args.get('startDate', '')
    end_date = request.args.get('endDate', '')

    database_connection = get_database_connection()

    cursor = database_connection.cursor()
    if is_datetime_iso_valid(start_date) and is_datetime_iso_valid(end_date):
        cursor.execute('SELECT * FROM drones WHERE seen_on >= %s AND seen_on <= %s',
                       (start_date, end_date))
    else:
        date_today = str(datetime.now().date())
        cursor.execute('SELECT * FROM drones WHERE seen_on >= %s AND seen_on <= %s',
                       (f'{date_today}T00:00:00.000Z', f'{date_today}T23:59:59.999Z'))

    data = cursor.fetchall()
    print("Drones data: ", data)

    # Closing the connection
    database_connection.close()

    return "Drones data: " + str(data)


@app.post('/report')
def report():
    start_date = request.args.get('startDate', '')
    end_date = request.args.get('endDate', '')

    # add S3 check if such report has already been generated earlier and return it

    if not is_datetime_iso_valid(start_date) and not is_datetime_iso_valid(end_date):
        date_today = str(datetime.now().date())
        start_date = f'{date_today}T00:00:00.000Z'
        end_date = f'{date_today}T23:59:59.999Z'

    response = get_drones_data_by_date_range(start_date, end_date)
    data = response.json().get('rows')

    report = generate_drones_json_report(start_date, end_date, data)
    report_save_result = save_drones_report(report)
    return {"reportUrl": report_save_result.get("objectUrl")}


if __name__ == "__main__":
    app.run()
