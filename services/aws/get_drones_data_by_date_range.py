import os
from dotenv import load_dotenv
import requests

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))

AWS_LAMBDA_API_GATEWAY_URL = os.getenv(
    'AWS_LAMBDA_API_GATEWAY_URL')
AWS_LAMBDA_API_GATEWAY_STAGE = os.getenv(
    'AWS_LAMBDA_API_GATEWAY_STAGE')


def get_drones_data_by_date_range(start_date='', end_date=''):
    try:
        return requests.get(
            f"{AWS_LAMBDA_API_GATEWAY_URL}/{AWS_LAMBDA_API_GATEWAY_STAGE}/drones?startDate={start_date}&endDate={end_date}")
    except:
        raise Exception("Sorry, error")
