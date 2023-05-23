import os
from dotenv import load_dotenv
import requests

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))

AWS_LAMBDA_API_GATEWAY_URL = os.getenv(
    'AWS_LAMBDA_API_GATEWAY_URL')
AWS_LAMBDA_API_GATEWAY_STAGE = os.getenv(
    'AWS_LAMBDA_API_GATEWAY_STAGE')


def save_drones_report(report):
    try:
        result = requests.post(
            f"{AWS_LAMBDA_API_GATEWAY_URL}/{AWS_LAMBDA_API_GATEWAY_STAGE}/reports", data=report)
        return result.json()
    except:
        raise Exception("Sorry, error")
