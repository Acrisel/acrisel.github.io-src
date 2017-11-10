:title: Remote Host Accessibility
:slug: python-check-remote-host-accessibility
:date: 2017-09-24 20:47
:authors: Arnon Sela
:tags: Python, Network, Distributed

----------------------------------------------
How to check port on remote host is accessible 
----------------------------------------------

Synopsis
========

This post shows how to validate remote host is accessible.

Motivation
==========

There are many solutions out there on how to check that port on a remote host is accessible. But we needed a solution that would not hang up.

Checking Remote Port
====================

Here is the code that does the job:

    .. code-block:: python
    
        import socket
        
        def port_is_open(host, port, timeout=0.5):
            result = False
            try:
                s = socket.create_connection((host, port), timeout)
            except socket.error as e:
                pass
            else:
                s.close()
                result = True
            return result
        
The check how it performs, we will use the *timeit* function shown here:

    .. code-block:: python
    
        import time
        
        def timeit(func, *args, **kwargs):    
            start_time = time.time()
            result = func(*args, **kwargs)
            print("returned %s in %s seconds" % (result, time.time() - start_time))
    
The result of checking that port on a remote host is accessible, and another that is not:

    .. code-block:: python
    
        >>> timeit(port_is_open, "192.168.1.100", 22)
        returned True in 0.0007190704345703125 seconds
        >>> timeit(port_is_open, "192.168.1.70", 22)
        returned False in 0.5032269954681396 seconds
    

Conclusion
==========

It cannot be easier, yea?!

Note: checking a port on remote host may be impacted by many things, predominantly how busy the network is and how busy are the involved hosts.  Therefore, the timeout may need to be adjusted according to the operational environment.

References
==========

   | `Python's socket library <https://docs.python.org/3/library/socket.html>`__
