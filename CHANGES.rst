Version 0.2.1
=============

Released 2018-06-27

- Revert regression introducted in an attempt to address exceptions being swallowed. _begin_consuming reverted to not return the loop.create_task 

Version 0.2.0
=============

Released 2018-06-25

- Update Henson-SQS to use asyncio coroutines for sending and receiving
  messages as required by Henson>=0.5.0 (*Backwards Incompatible*)
- Register a message acknowledgement callback to delete the incoming message
  from the queue after processing has finished
- Remove the ``SQS_DELETE_MESSAGES_ON_READ`` setting
- Make queue URL and AWS credentials settings optional
- Bugfix: postpone internal message queue creation until it's needed by the
  `_consume` function
- Bugfix: _begin_consuming needs to return the future, otherwise the excpetions are not bubbled up to Henson


Version 0.1.1
=============

Released 2015-11-30

- Delete messages from SQS queue before yielding (*Backwards Incompatible*)


Version 0.1.0
=============

Released 2015-10-22

- Initial release
