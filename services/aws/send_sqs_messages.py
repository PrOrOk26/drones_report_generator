import logging
import sys

import boto3
from botocore.exceptions import ClientError

sqs_client = boto3.client('sqs')

logger = logging.getLogger(__name__)


def send_sqs_messages(queue_url, message):
    """
    Send a batch of messages in a single request to an SQS queue.
    This request may return overall success even when some messages were not sent.
    The caller must inspect the Successful and Failed lists in the response and
    resend any failed messages.

    :param queue: The queue to receive the messages.
    :param messages: The messages to send to the queue. These are simplified to
                     contain only the message body and attributes.
    :return: The response from SQS that contains the list of successful and failed
             messages.
    """
    try:
        response = sqs_client.send_message(
            QueueUrl=queue_url, MessageBody=message['body'], MessageAttributes=message['attributes'])
        if 'Successful' in response:
            logger.info(
                "Message sent!"
            )
        if 'Failed' in response:
            logger.warning(
                "Failed to send!")
    except ClientError as error:
        logger.exception("Send messages failed to queue: %s", "Test queue")
        raise error
    else:
        return response


# def get_queues(prefix=None):
#     """
#     Gets a list of SQS queues. When a prefix is specified, only queues with names
#     that start with the prefix are returned.

#     :param prefix: The prefix used to restrict the list of returned queues.
#     :return: A list of Queue objects.
#     """
#     if prefix:
#         queue_iter = sqs.queues.filter(QueueNamePrefix=prefix)
#     else:
#         queue_iter = sqs.queues.all()
#     queues = list(queue_iter)
#     if queues:
#         logger.info("Got queues: %s", ', '.join([q.url for q in queues]))
#     else:
#         logger.warning("No queues found.")
#     return queues
