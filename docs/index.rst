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

===============================    ============================================
``AWS_ACCESS_KEY``                 The access key used to connect to AWS.
                                   default: ``None``
``AWS_ACCESS_SECRET``              The access secret used to connect to AWS.
                                   default: ``None``
``AWS_REGION_NAME``                The AWS region to use.
                                   default: ``None``
``SQS_INBOUND_QUEUE_URL``          The URL representing the SQS queue to be
                                   used for inbound messages.
                                   required
``SQS_OUTBOUND_QUEUE_URL``         The URL representing the SQS queue to be
                                   used for outbound messages.
                                   required
``SQS_ATTRIBUTE_NAMES``            A list of names of metadata attributes to be
                                   fetched with inbound queue messages.
                                   default: ``['All']``
``SQS_MESSAGE_ATTRIBUTE_NAMES``    A list of message attributes to be fetched.
                                   default: ``['All']``
``SQS_MESSAGE_BATCH_SIZE``         Number of messages to be fetched with each.
                                   call to SQS.
                                   default: ``10``
``SQS_VISIBILITY_TIMEOUT``         How long (in seconds) a message should be
                                   hidden from subsequent retrievals before
                                   becoming available for consumption again.
                                   default: ``60``
``SQS_WAIT_TIME``                  How long (in seconds) calls to
                                   ``receive_message`` should wait before
                                   returning if no messages are in the queue.
                                   default: ``20``
===============================    ============================================

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

