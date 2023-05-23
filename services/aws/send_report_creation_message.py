import logging
import sys
import boto3
from botocore.exceptions import ClientError

from services.aws.send_sqs_messages import send_sqs_messages

logger = logging.getLogger(__name__)

sqs_client = boto3.client('sqs')

queue = sqs_client.get_queue_url(QueueName='ReportCreationEvents')


def send_report_creation_message(reportUrl):
    message = {"body": f"Hey <USER NAME AND SURNAME THAT I WOULD NEED TO GET SOMEWHERE>, here is a link {reportUrl}. This report has just been generated!",
               "attributes": {"ReportType": {'DataType': 'String', "StringValue": "on_demand_report"}, "reportUrl": {'DataType': 'String', "StringValue": reportUrl}}
               }

    send_sqs_messages(queue_url=queue['QueueUrl'], message=message)
