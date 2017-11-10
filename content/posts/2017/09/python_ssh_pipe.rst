:title: SSH Pipe with Python's Subprocess
:slug: ssh-pipe-with-python-subprocess
:date: 2017-09-06 12:09
:authors: Arnon Sela
:tags: Python, Subprocess, SSH, Pipe, pipeline, distributed

----------------------------------------------
How to pass objects to remote system using SSH
----------------------------------------------

Synopsis
========

This post shows how to create pipe channel over SSH. In particular, it demonstrates how to instantiate pipeline channel over SSH. We use this channel to pass an object to a remote system.  This post shows two methods. One using named-pipe and the other using unnamed-pipe.

Motivation
==========

We needed a simple mechanism to pass objects between hosts on a cluster. The goal was to have a secured process but without the need to establish and maintain ports for communications. Managing firewalls became bureaucratic headake. Therefore, we opt to use SSH as the security medium for the channel.

SSH Settings
============

Security needs to be arranged using SSH public and private keys.
Moreover, the account under which SSH channel will be established should be set correctly so SSH invocation would include environment settings.

1. Create ~/.ssh_profile:

    .. code-block:: python

        # what ever setting needed, similar to .profile
        # and, source virtualenv for the connection
        source /path/to/virtualenv/bin/activate

#. Update ~/.ssh/authorized_keys:

    .. code-block:: python

        command=". ~/.ssh_profile; if [ -n \"$SSH_ORIGINAL_COMMAND\" ];
        then eval \"$SSH_ORIGINAL_COMMAND\"; else exec \"$SHELL\"; fi" ssh-rsa ...

Note that there are multiple ways to accomplish what the above steps do.  For example, you can remove the ability to get command prompt via SSH.  Or you can source directly ~/.profile.  The key requirement is to be able to send a command via SSH and have the environment for that command to be arranged automatically.

The object
==========

This example uses simple object of class *RemoteWorker* that would be passed to a remote engine to be acted upon.  *RemoteWorker* has a simple method, *run()* that writes 'Hello' to stdout.

.. _RemoteWorker:

.. code-block:: python

    class RemoteWorker(object):
        def __init__(self):
            pass

        def run(self):
            print("Hello")

Using Named-pipe
================

Main program (below) starts with creating named-pipe (using *mkfifo*).  It then forks a child process where SSH channel will be established.  The child function *remote_agent* process starts sshagent_namedpipe.py_ which under SSH.  This program will run on the remote host and will accept the object send to it by *send_workload_to_agent* function which is called by the parent process.

.. code-block:: python

    from concepts.sshcmd import sshcmd
    import pickle
    import os
    from concepts.sshtypes import RemoteWorker

    def remote_agent(pipe_name, host, agentpy):
        pipein = open(pipe_name, 'rb')
        remote = sshcmd(host, "python " + agentpy, stdin=pipein)

        if remote.returncode != 0:
            raise Exception(remote.stderr.decode())
        return remote.stdout

    def send_workload_to_agent(pipe_name):
        pipeout = open(pipe_name, 'wb')
        worker = RemoteWorker()
        workload = pickle.dumps(worker)
        pipeout.write(workload)

    if __name__ == '__main__':
        mp.freeze_support()
        mp.set_start_method('spawn')

        pipe_name = 'ssh_pipe'

        if not os.path.exists(pipe_name):
            # creating namedpipe
            os.mkfifo(pipe_name)

        pid = os.fork()
        if pid == 0:
            # child process
            agent_dir = "/path/to/program/directory"
            agentpy = os.path.join(agent_dir, "sshagent_namedpipe.py")
            msg = remote_agent(pipe_name, '192.168.1.70', agentpy)
            print("from remote: %s" % msg.decode())
            exit()

        send_workload_to_agent(pipe_name)
        pid, status = os.waitpid(pid, os.WNOHANG)

Notes:

    1. sshagent_namedpipe.py_ is assumed to be installed on the remote host.
    #. *remote_agent* function opens named-pipe for reading and passes it to a remote process.
    #. sshcmd_ function establishes the SSH connection via subprocess (can be found here: sshcmd_).
    #. *local_host* function opens named-pipe to write, pickles RemoteWorker_ object, and passes it to the pipe.

.. _sshcmd: https://acrisel.github.io/posts/2017/08/ssh-made-easy-using-python/

.. _sshagent_namedpipe.py:

.. code-block:: python

    import pickle
    import sys

    # need to import objects that would be passed with in
    from concepts.sshtypes import RemoteWorker

    workload = sys.stdin.buffer.read()
    worker = pickle.loads(workload)
    worker.run()

Notes:

    1. sshagent_namedpipe.py_ simply reads the pickled representation of RemoteWorker_.
    #. it then invokes its *run()* method.

Using Pipe
==========

The one drawback of named-pipe is that it leaves a footprint on the filesystem. That footprint of named-pipe needs to be taken care of.
An alternative to named-pipe is a unnamed-pipe or just pipe.  It's a bit more complicated to handle for passing objects via SSH, but not by too much.

The concept is similar; we need to create a pipe with reader and writer on its ends. This time we will use *os.pipe()*, instead of *mkfifo*.

.. code-block:: python

    import pickle
    import os
    import struct
    from concepts.sshcmd import sshcmd
    from concepts.sshtypes import RemoteWorker

    def get_pipe():
        pipein, pipeout = os.pipe()
        pipe_reader = os.fdopen(pipein, 'rb')
        pipe_writer = os.fdopen(pipeout, 'wb')
        return pipe_reader, pipe_writer

    def remote_agent(host, agentpy, pipein):
        remote = sshcmd(host, "python " + agentpy, stdin=pipein)

        if remote.returncode != 0:
            print(remote.stderr.decode())

        return remote.stdout

    def send_workload_to_agent(pipeout):
        worker = RemoteWorker()
        workload = pickle.dumps(worker)
        msgsize = len(workload)
        pipeout.write(struct.pack(">L", msgsize))
        pipeout.write(workload)

    if __name__ == '__main__':
        mp.freeze_support()
        mp.set_start_method('spawn')

        pipein, pipeout = get_pipe()

        pid = os.fork()
        if pid == 0:
            # child process
            agent_dir = "/path/to/program/directory"
            agentpy = os.path.join(agent_dir, "sshagent_pipe.py")
            msg = remote_agent( '192.168.1.70', agentpy, pipein)
            print("from remote: %s" % msg.decode())
            exit()

        send_workload_to_agent(pipeout)
        pid, status = os.waitpid(pid, os.WNOHANG)

Notes:

    1. The function *get_pipe()* opens a pipe and creates reader and writer file descriptors to it. File descriptors allow the pipe to be treated as stdin and stdout respectively.
    #. The other main change is that *send_workload_to_agent* function sends the length of the pickled object before sending the object itself.  The pickled object size is packed before sending it over.
    #. Last, the child process runs sshagent_pipe.py_ Instead of its sibling sshagent_namedpipe.py_.

.. _sshagent_pipe.py:

.. code-block:: python

    import pickle
    import sys
    import struct
    from concepts.sshtypes import RemoteWorker

    msgsize_raw = sys.stdin.buffer.read(4)
    msgsize = struct.unpack(">L", msgsize_raw)
    workload = sys.stdin.buffer.read(msgsize[0])

    worker = pickle.loads(workload)
    worker.run()

Notes:

    1. The agent pipe version first reads and unpacks the size of the object being transferred.
    #. It then reads the pickled object and invokes its action.

Conclusion
==========

Both named-pipe and pipe version of SSH object communication is workable.  Both named-pipes and unnamed-pipes would do the job.  My personal preference is the unnamed-pipe solution due to the absence of filesystem footprint.

However, os.fork and os.pipe are not supported on all platforms.  This mechanism will work for Linux based systems (including os x), but not on Windows.  Next post on this subject will show how to accomplish the same using Multiprocessing package which supports Windows.

References
==========

   | ssh command: sshcmd_
   