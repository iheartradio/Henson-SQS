"""SQS plugin for Henson."""

import asyncio
from contextlib import suppress
from pkg_resources import get_distribution
import json

from boto3.session import Session
from henson import Extension
from lazy import lazy


__all__ = ('SQS',)
__version__ = get_distribution(__package__).version


class Consumer:
    """A consumer of an SQS queue.

    For each message consumed from the queue, the specified callback
    will be called.

    Args:
        app (henson.base.Application): The app instance registered to
            the SQS extension.
        client (boto3.SQS.Client): The SQS client that should be used
            for connections.

    .. versionchanged:: 0.2.0

        All parameters passed to ``__init__`` other than ``client`` were
        replaced with a reference to an
        :class:`~henson.base.Application`. These parameters previously
        took values from ``app.settings``; ``app.settings`` is now used
        directly.
    """

    def __init__(self, app, client):
        """Initialize the consumer."""
        self.app = app
        self.client = client
        self.app.message_acknowledgement(self.acknowledge_message)

    @asyncio.coroutine
    def acknowledge_message(self, app, message):
        """Delete a message from the SQS inbound queue.

        Args:
            app (henson.base.Application): The application that
                processed the message.
            message (dict): The message returned from the consumer to
                the application.
        """
        self.client.delete_message(
            QueueUrl=self.app.settings['SQS_INBOUND_QUEUE_URL'],
            ReceiptHandle=message['ReceiptHandle'],
        )

    @asyncio.coroutine
    def read(self):
        """Read a single message from the message queue.

        Returns:
            dict: A JSON-decoded message.
        """
        message = None
        while message is None:
            messages = self.client.receive_message(
                QueueUrl=self.app.settings['SQS_INBOUND_QUEUE_URL'],
                AttributeNames=self.app.settings['SQS_ATTRIBUTE_NAMES'],
                MessageAttributeNames=self.app.settings['SQS_MESSAGE_ATTRIBUTES'],
                # TODO: It would be nice if this was configurable.
                MaxNumberOfMessages=1,
                VisibilityTimeout=self.app.settings['SQS_VISIBILITY_TIMEOUT'],
                WaitTimeSeconds=self.app.settings['SQS_WAIT_TIME'],
            )

            with suppress(IndexError, KeyError):
                message = messages['Messages'][0]
                message['Body'] = json.loads(message['Body'])
        return message


class Producer:
    """A producer to write to an SQS queue.

    Args:
        app (henson.base.Application): The app instance registered to
            the SQS extension.
        client (boto3.SQS.Client): The client with which to write
            messages.

    .. versionchanged:: 0.2.0

        All parameters passed to ``__init__`` other than ``client`` were
        replaced with a reference to an
        :class:`~henson.base.Application`. These parameters previously
        took values from ``app.settings``; ``app.settings`` is now used
        directly.
    """

    def __init__(self, app, client):
        """Initialize the producer."""
        self.app = app
        self.client = client

    @asyncio.coroutine
    def send(self, message, delay=0, message_attributes=None):
        """Send the message to the queue.

        Args:
            message (dict): The message to send.
            delay (int): The number of seconds until the message becomes
              consumable from the queue.
            message_attributes (dict): Attributes to be send along with
              the message body.
        """
        if message_attributes is None:
            message_attributes = {}
        return self.client.send_message(
            QueueUrl=self.app.settings['SQS_OUTBOUND_QUEUE_URL'],
            MessageBody=json.dumps(message),
            DelaySeconds=delay,
            MessageAttributes=message_attributes,
        )


class SQS(Extension):
    """An interface to interact with an SQS queue.

    Args:
        app (Optional[henson.base.Application): An application instance
            that has an attribute named settings that contains a mapping
            of settings to interact with SQS.
    """

    DEFAULT_SETTINGS = {
        'SQS_ATTRIBUTE_NAMES': ['All'],
        'SQS_MESSAGE_ATTRIBUTES': ['All'],
        'SQS_MESSAGE_BATCH_SIZE': 10,
        'SQS_VISIBILITY_TIMEOUT': 60,
        'SQS_WAIT_TIME': 20,
    }

    REQUIRED_SETTINGS = (
        'AWS_ACCESS_KEY',
        'AWS_ACCESS_SECRET',
        'AWS_REGION_NAME',
        'SQS_INBOUND_QUEUE_URL',
        'SQS_OUTBOUND_QUEUE_URL',
    )

    @lazy
    def client(self):
        """Return the connection to SQS.

        Returns:
            boto3.SQS.Client: A connection to the SQS service.
        """
        session = Session(
            aws_access_key_id=self.app.settings['AWS_ACCESS_KEY'],
            aws_secret_access_key=self.app.settings['AWS_ACCESS_SECRET'],
            region_name=self.app.settings['AWS_REGION_NAME'],
        )
        return session.client('sqs')

    def consumer(self):
        """Return a new SQS consumer.

        Returns:
            Consumer: The new consumer.
        """
        return Consumer(app=self.app, client=self.client)

    def producer(self):
        """Return a new SQS producer.

        Returns:
            Producer: The new producer.
        """
        return Producer(app=self.app, client=self.client)
