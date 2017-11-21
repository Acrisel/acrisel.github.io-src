:title: SSH Pipe with Python's Subprocess and Multiprocessing
:slug: ssh-pipe-with-python-subprocess_multiprocessing
:date: 2017-09-13 22:55
:modified: 2017-09-27 08:22
:authors: Arnon Sela
:tags: Python, Subprocess, SSH, Pipe, pipeline, distributed, Multiprocessing, fdopen, dup

------------------------------------------------------------------
How to pass objects to remote system using SSH and Multiprocessing
------------------------------------------------------------------

Synopsis
========

Previous post_ on this subject used os.fork and os.pipe to issue SSH in a child process. Instead, this post uses multiprocessing Process and Pipe to make it more platform agnostic.  Per audience request, this post will also make use of more object oriented techniques.

.. _post: https://acrisel.github.io/posts/2017/09/ssh-pipe-with-python-subprocess/

Motivation
==========

A real scenario of using SSH pipeline includes more than just the two endpoints. For example, the initiating end might pass multiprocessing queues to its child process. Such queues can be used to exchange status and controls. Additionally, os.fork is not supported on all platforms.  It would then be beneficial if we use multiprocessing Process and Pipe instead of os.fork and os.pipe respectively.

In this post, we will focus on portable artifacts.

Assumptions
===========

Assuming SSH setting and Workload object (class *RemoteWorker*) are same as in the previous post_.

SSH with Multiprocessing Pipe
=============================

The one drawback of os.fork and os.pipe is that they are not supported on all platforms.  For example, os.fork is supported on Unix only. Also, os.fork makes it somewhat more complicated system based objects from parent to child. Hence, we use here multiprocessing Process and Pipe.

The concept here is similar to the one previous post_; we need to create a pipe with reader and writer on its ends. This time we will use *multiprocessing.Pipe()* and *multiprocessing.Process().  One major difference is the bundling of *agent* functions into a class *SSHPipe*.

*multiprocessing.Pipe()* uses *send()* and *recv()* methods to write and read information to the pipe. Since we want to pass pipe reading side as stdin to *subprocess*, we need need to translate pipe reading end to a regular file. If we do that to one end, we need to do the same to the other end. We accomplish this by using fdopen.

.. code-block:: python

    import os
    import pickle
    from subprocess import run, PIPE
    import sshtypes # where RemoteWorker is defined
    import multiprocessing as mp

    class SSHPipe(object):
        def __init__(self, host, agent_program, user=None,):
            self.pipe_read, self.pipe_write = mp.Pipe()
        
            self.__communicateq = mp.Queue()
            self.agent_program = agent_program
            self.where = "%s%s" % ('' if user is None else "@%s" % user, host)            
            self.result = None
            
        def start(self, wait=None):
            self.__agent =  mp.Process(target=self.run_agent, 
                args=(self.where, self.agent_program, self.pipe_read, self.pipe_write, self.__communicateq), 
                daemon=True) 
            try:
                self.__agent.start()
            except Exception:
                raise
        
            if wait is not None:
                while True:
                    time.sleep(wait)
                    if self.__agent.is_alive() or self.__agent.exitcode is not None:
                        break

            self.pipe_read.close()
        
        def run_agent(self, where, agent_program, pipe_read, pipe_write, communicateq):
            pipe_write.close()
            pipe_readf = os.fdopen(os.dup(pipe_read.fileno()), 'rb')
        
            cmd = ["ssh", where, 'python', agent_program]
            sshrun = run(cmd, shell=False, stdin=pipe_readf, stdout=PIPE, stderr=PIPE, check=False,)
            response = (sshrun.returncode, sshrun.stdout.decode(), sshrun.stderr.decode())
            communicateq.put(response)
            pipe_readf.close()
        
        def __prepare(self, msg, pack=True):
            workload = msg
            if pack:
                workload = pickle.dumps(msg)
            msgsize = len(workload)
            magsize_packed = struct.pack(">L", msgsize)
            return magsize_packed + workload
    
        def is_alive(self):
            return self.__agent.is_alive()
    
        def send(self, msg, pack=True):
            pipe_writef = os.fdopen(os.dup(self.pipe_write.fileno()), 'wb')
            request = self.__prepare(msg, pack=pack)
            pipe_writef.write(request)
            pipe_writef.close()
        
        def response(self, timeout=None):
            if self.result is None:
                try:
                    result = self.__communicateq.get(timeout=timeout)
                except:
                    pass
                if result:
                    self.result = result[0], result[1], result[2]
            return self.result
        
        def close(self):
            if self.is_alive():
                self.send('TERM')
            response = self.response()
            self.__agent.join()
            return response
        
Notes:

1. *run_agent()* in *cmd* parameter is using *'python'* as a medium to run *agent_command*. If *agent_command* is executable and is reachable by *PATH*, then *'python'* can be omitted.
#. *start()* method launches *run_agent()* as a child process, then *send()* is used to write to pipe.
#. *run_agent()* child process push response back to parent using *Queue* (*communicateq*).
#. *close()* method is used to close the pipe and send response back.
#. or, *response()* method can be used to fetch response off the SSH pipe.

Finally, *sshremoteagent.py* is unchanged in concept from its original pipe form in the previous post_. This version uses a loop to allow multiple objects to be passed.  Loop will end cleanly once  *TERM* is received.

.. _sshremoteagent.py:

.. code-block:: python

    #!/usr/bin/env python
    import sshtypes 
    import pickle
    import sys
    import struct

    while True:
        try:
            msgsize_raw = sys.stdin.buffer.read(4)
            msgsize = struct.unpack(">L", msgsize_raw)
            workload = sys.stdin.buffer.read(msgsize[0])
            worker = pickle.loads(workload)
        except Exception as e:
            print(e, file=sys.stderr)
            print("TERM")
            exit(1)
    
        if not isinstance(worker, str): 
            worker.run()
        elif worker == 'TERM':
            # maybe worker prints to stdout
            exit(0)
        else:
            print("Bad worker: " + repr(worker), file=sys.stderr)
            print("TERM")
            exit(2)

Notes:

1. *stdout* and *stderr* of *sshremoteagent* are linked to SSH, therefore, errors are written to stderr.
#. Return message to SSH Pipe is done via stdout of the remote agent process. The response is transfer once the remote agent ends.
#. If agent encounters an error, it exits with exitcode 1 or 2 according to the type of error.  
#. Agent also prints out the word *TREM*, notifying of its termination, as well as an error message to *stderr* in case of an error.
    
Example usage
=============

.. code-block:: python

    import sshtypes
    
    mp.set_start_method('spawn')
    
    agent_dir = "/path/to/program/directory"
    agentpy = os.path.join(agent_dir, "sshremoteagent.py")
    host = '192.168.1.100' # remote host IP address, or better yet, use host by name.
    
    sshagent = SSHPipe(host, agentpy)
    sshagent.start()
    
    if not sshagent.is_alive():
        print(sshagent.response())
        exit(1)
        
    worker = sshtypes.RemoteWorker()
    sshagent.send(worker)
    
    if not sshagent.is_alive():
        print(sshagent.response())
        exit()

    sshagent.send(worker)

    response = sshagent.close()
    print('response: ', response)


Additional thoughts
===================

Using multiprocessing version of SSH pipe banks on its support of multiple platforms. The example usage was made simple.  It can be made more sophisticated (and should be) using *try-except* clauses. As well as better consideration of the response. 

One issue stands out is that remote agent transfers all information at the end of processing. In fact, this might be different on different platforms. One way to work around this is to send back information using another SSH channel in the reversed direction. 

In this scenario, the remote agent would start SSH callback agent with source system. When information needs to be passed back to the source, the remote agent will use the callback channel to activate 'response workers'.

References
==========

   | ssh namedpipes and pipes post_

