:title: SSH Made Easy Using Python Subprocess
:slug: ssh-made-easy-using-python
:date: 2017-08-22 23:12:44
:modified: 2017-09-02 16:10
:authors: Arnon Sela
:tags: Python, SSH, subprocess, distributed, cluster

-----------------
Subprocess Module
-----------------

Synopsis
========

Python's subprocess module makes it easy to invoke external commands on localhost.  It can also use SSH to invoke commands on remote hosts.


How simple?
===========

The short answer is, very simple!

The longer answer is, subprocess.run, as follows:

    .. code-block:: python

        result = subprocess.run(["ssh", "some-host@some-user", "some-command"],
                                shell=False,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                check=False)

Prerequisites
=============

For subprocess ssh-run to work, ssh configuration needs to be in place. This means that:

    1. ssh-keygen on originating machine
    #. ssh-copy-id to the target machine into the target account's .ssh/authorized_keys
    #. optional: create .ssh/config for easier ssh call
    #. optional: use *command* in target .ssh/authorized_keys to allow proper setup, if needed, e.g:

        .. code-block:: python

            command="if [[ \"x${SSH_ORIGINAL_COMMAND}x\" != \"xx\" ]]; then source ~/.profile; eval \"${SSH_ORIGINAL_COMMAND}\"; else /bin/bash --login; fi;" <ssh_key>
            
Note that if you use bash, .profile may be .bash_profile. If you don't use bash, an appropriate shell profile should be sourced.

Wrapper
=======

    .. code-block:: python

        def sshcmd(host, command, user=None, stdin=None, check=False):
            ''' Runs ssh command via subprocess.  Assuming .ssh/config is configured.

            Args:
                host: target host to send the command to
                command: command to run on the host
                user: (optional) user to use to login to host
                stdin: (optional) override sys.stdin
                check: (optional) pass to *subprocess.run*; if set, checks return code
                    and raises subprocess.CalledProcessError, if none-zero result

            Returns:
                subprocess.CompletedProcess object
            '''

            where = "%s" % host if user is None else "%s@%s" %(user, host)
            result = subprocess.run(["ssh", where, command],
                                   shell=False,
                                   stdin=stdin,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   check=check)
            return result

        if __name__ == '__main__':
            # will work on if you have a host named ubly with ssh configuration
            out = sshcmd("ubly", "ls -l", check=False).stdout.decode()

Note the following:

    1. *check=True* would cause subprocess.run to through *subprocess.CalledProcessError*, if ssh exits with error code (greater than 0).
    #. sshcmd returns *subprocess.CompletedProcess*; which gives full access to *PIPEs* and *return-code*.
    #. stdout and stderr attributes are of binary form. Therefore result needs to be *decoded()*.
