:title: Paradigm for Distributed Logging
:slug: paradigm-for-distributed-logging
:date: 2017-10-24 20:47
:authors: Arnon Sela
:tags: Python, Network, Logging, Log, Distributed

------------------------------------------
Getting logging in distributed environment
------------------------------------------

Synopsis
========


Motivation
==========

Python has a very nice logging package. That is until you try to work it over distributed environment. In particular, the socket based logging mechanism and its examples are not robust enough to be used in a more complex environment. If you try, you will find that not all messages are ending in logs. Or that process does not end.

.. _`SSH agents`: https://acrisel.github.io/posts/2017/09/ssh-pipe-with-python-subprocess_multiprocessing/
.. _`Sending and receiving logging events across a network`: https://docs.python.org/3.6/howto/logging-cookbook.html#logging-cookbook

Driving architecture
--------------------

The architecture is of that a server process submit processing in multiple machines. Remote process send back logging data.

.. image:: |filename|/images/python_distributed_logging/driving_architecture.png
    :alt: driving architecture flow;

The mechanism assums that beside SSH ports, no other port can be opend and dedicated to logging. Therefore, cross node links are assumed to be SSH channels.

Example use
-----------

Here is a simplistic example for which we needed the logging environment to work. In this example, client is local. However, we use SSH channels based on `SSH agents`_ to pass logging information between hosts. This example is adopted from `Sending and receiving logging events across a network`_.

    .. code-block:: python

        from nwlogger import NwLogger
        import multiprocessing as mp
        import logging

        def log(logger_info):
            logger1 = NwLogger.get_logger(logger_info, name='example.e1')
            logger2 = NwLogger.get_logger(logger_info, name='example.e2')

            logger2.info('How quickly daft jumping zebras vex.')
            logger1.warning('Jail zesty vixen who grabbed pay from quack.')
            logger1.debug('Quick zephyrs blow, vexing daft Jim.')
            logger2.error('The five boxing wizards jump quickly.')

        def main():
            nwlogger = NwLogger('example', logging_level=logging.DEBUG, consolidate=True)
            nwlogger.start()

            logger_info = nwlogger.logger_info()
            logger = NwLogger.get_logger(logger_info=logger_info)
            logger.info('Jackdaws love my big sphinx of quartz.')

            client = mp.Process(target=log, args=(logger_info,))
            client.start()
            client.join()

            nwlogger.stop()

        if __name__ == '__main__':
            mp.freeze_support()
            mp.set_start_method('spawn')
            main()

The expected results from this example:

    .. code-block:: python

        2017-09-25 09:45:00.485: 2397   : INFO   : Jackdaws love my big sphinx of quartz.
        2017-09-25 09:45:00.551: 2400   : WARNING: Jail zesty vixen who grabbed pay from quack.
        2017-09-25 09:45:00.552: 2400   : DEBUG  : Quick zephyrs blow, vexing daft Jim.: nwlogger_example.log(16)
        2017-09-25 09:45:00.547: 2400   : INFO   : How quickly daft jumping zebras vex.
        2017-09-25 09:45:00.552: 2400   : ERROR  : The five boxing wizards jump quickly.

Note that messages are not printed in order. Reason is that the solution uses ThreadingTCPServer in which threads are open to read individual requests. Therefore order is not guarenteed.

Design
======



References
==========

   | `SSH agents`_
   | `Sending and receiving logging events across a network`_
