==========
Henson-SQS
==========

Provides SQS support to Henson Applications.

Quickstart
==========

.. code::

    from henson import Application
    from henson_sqs import SQS

    app = Application(__name__)
    sqs = SQS(app)

    app.consumer = sqs.consumer()

    def relay_message(app, data):
        producer = sqs.producer()
        producer.send('relayed', data)

    app.callback = relay_message


Configuration
=============

The following settings are used by Henson-SQS:

+----------------------------+------------------------------------------------+
| ``AWS_ACCESS_KEY``         | The access key used to connect to AWS.         |
|                            | Defaults to ``None``.                          |
+----------------------------+------------------------------------------------+
| ``AWS_ACCESS_SECRET``      | The access secret used to connect to AWS.      |
|                            | Defaults to ``None``.                          |
+----------------------------+------------------------------------------------+
| ``AWS_REGION_NAME``        | The AWS region to use. Defaults to ``None``.   |
+----------------------------+------------------------------------------------+
| ``SQS_INBOUND_QUEUE_URL``  | The URL representing the SQS queue to be used  |
|                            | for inbound messages. Required.                |
+----------------------------+------------------------------------------------+
| ``SQS_OUTBOUND_QUEUE_URL`` | The URL representing the SQS queue to be used  |
|                            | for outbound messages. Required.               |
+----------------------------+------------------------------------------------+
| ``SQS_PREFETCH_LIMIT``     | The maximum number of messages to keep in the  |
|                            | internal queue waiting to be processed. If set |
|                            | to ``0``, the queue size is unlimited.         |
|                            | Defaults to ``0``.                             |
+----------------------------+------------------------------------------------+
| ``SQS_ATTRIBUTE_NAMES``    | A list of names of metadata attributes to be   |
|                            | fetched with inbound queue messages. Defaults  |
|                            | to ``['All']``.                                |
+----------------------------+------------------------------------------------+
| ``SQS_MESSAGE_ATTRIBUTES`` | A list of message attributes to be fetched.    |
|                            | Defaults to ``['All']``.                       |
+----------------------------+------------------------------------------------+
| ``SQS_MESSAGE_BATCH_SIZE`` | The number of messages to be fetched with each |
|                            | call to SQS. Defaults to ``10``.               |
+----------------------------+------------------------------------------------+
| ``SQS_VISIBILITY_TIMEOUT`` | How long (in seconds) a message should be      |
|                            | hidden from subsequent retrievals before       |
|                            | becoming available for consumption again.      |
|                            | Defaults to ``60``.                            |
+----------------------------+------------------------------------------------+
| ``SQS_WAIT_TIME``          | How long (in seconds) calls to                 |
|                            | ``receive_message`` should wait before         |
|                            | returning if no messages are in the queue.     |
|                            | Defaults to ``20``.                            |
+----------------------------+------------------------------------------------+

Contents:

.. toctree::
   :maxdepth: 1

   api
   changes


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

