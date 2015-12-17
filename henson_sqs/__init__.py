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
    """

    def __init__(self, client, queue_url, attribute_names, message_attributes,
                 message_batch_size, visibility_timeout, wait_time,
                 delete_messages_on_read=True):
        """Initialize the consumer.

        Args:
            client (:class:`~boto3.SQS.Client`): the SQS client that
                should be used for connections
            queue_url (str): the SQS queue URL to read from
            attribute_names (List[str]): metadata attributes to return
                with each SQS message
            message_attribtue_names (List[str]): attributes of each
                message to be returned
            message_batch_size (int): the maximum number of messages to
                be retrieved with each call
            visibility_timeout (int): the number of seconds to hide
                the returned messages from subsequent retrieve queries
            wait_time (int): the maximum amount of time to wait for
                new messages
        """
        self.client = client
        self.queue_url = queue_url
        self.attribute_names = attribute_names
        self.message_attributes = message_attributes
        self.message_batch_size = message_batch_size
        self.visibility_timeout = visibility_timeout
        self.wait_time = wait_time
        self.delete_messages_on_read = delete_messages_on_read

    @asyncio.coroutine
    def read(self):
        """Read a single message from the message queue.

        Returns:
            dict: A JSON-decoded message.
        """
        message = None
        while message is None:
            messages = self.client.receive_message(
                QueueUrl=self.queue_url,
                AttributeNames=self.attribute_names,
                MessageAttributeNames=self.message_attributes,
                # MaxNumberOfMessages=self.message_batch_size,
                MaxNumberOfMessages=1,
                VisibilityTimeout=self.visibility_timeout,
                WaitTimeSeconds=self.wait_time,
            )

            with suppress(IndexError, KeyError):
                message = messages['Messages'][0]
                message['Body'] = json.loads(message['Body'])
                # TODO: once Henson support message acknowledgement,
                # this should be happen there instead.
                if self.delete_messages_on_read:
                    self.client.delete_message(
                        QueueUrl=self.queue_url,
                        ReceiptHandle=message['ReceiptHandle'],
                    )
        return message


class Producer:
    """A producer to write to an SQS queue.

    Args:
        client (:class:~boto3.SQS.Client): The client with which to
          write messages.
        queue_url (str): The URL representing the SQS queue to which the
          message should be written.
    """

    def __init__(self, client, queue_url):
        """Initialize the producer."""
        self.client = client
        self.queue_url = queue_url

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
            QueueUrl=self.queue_url,
            MessageBody=json.dumps(message),
            DelaySeconds=delay,
            MessageAttributes=message_attributes,
        )


class SQS(Extension):
    """An interface to interact with an SQS queue.

    Args:
        app (optional): An application instance that has an attribute
          named settings that contains a mapping of settings to interact
          with SQS.
    """

    DEFAULT_SETTINGS = {
        'SQS_ATTRIBUTE_NAMES': ['All'],
        'SQS_DELETE_MESSAGES_ON_READ': True,
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
            :class:`~boto3.SQS.Client`: A connection to the SQS service.
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
            :class:`Consumer`: The new consumer.
        """
        settings = self.app.settings
        return Consumer(
            client=self.client,
            queue_url=settings['SQS_INBOUND_QUEUE_URL'],
            attribute_names=settings['SQS_ATTRIBUTE_NAMES'],
            message_attributes=settings['SQS_MESSAGE_ATTRIBUTES'],
            message_batch_size=settings['SQS_MESSAGE_BATCH_SIZE'],
            visibility_timeout=settings['SQS_VISIBILITY_TIMEOUT'],
            wait_time=settings['SQS_WAIT_TIME'],
            delete_messages_on_read=settings['SQS_DELETE_MESSAGES_ON_READ'],
        )

    def producer(self):
        """Return a new SQS producer.

        Returns:
            :class:`Producer`: The new producer.
        """
        return Producer(
            client=self.client,
            queue_url=self.app.settings['SQS_OUTBOUND_QUEUE_URL']
        )
