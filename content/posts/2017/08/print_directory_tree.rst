:title: Print Directory Tree
:slug: print-directory-tree
:date: 2017-08-09 23:01:44
:athuors: Arnon Sela
:tags: OS, Utilities, Linux, Unix, Python

====================
Print Directory Tree
====================

----------------------------
Mimicking Linux Tree Utility
----------------------------

Introduction
============

Many blogs are showing how to print directory tree using Python.
Drawing from those examples, we built our version.  The primary drivers were:

    1. Compatability with Python3
    #. Print symbolic links
    #. Limit depth of tree

Function Code
==============

    I will refrain from going over the code, otherwise self-explanatory,  except mentioning the following:
        1. os.walk treats symbolic links per their target.  Therefore, a symbolic link may appear in dirs and files.
        #. only two main features of *tree* are replicated:  accepting both a root path and depth to explore.

    .. code-block:: python

        import os

        def realname(path, root=None):
            ''' joins root with path, if root is provided.
            Then check is it is a symlink.  If it is, return a string representing the link.  Otherwise, return
            basename or path.
            '''
            if root is not None:
                path=os.path.join(root, path)
            result=os.path.basename(path)
            if os.path.islink(path):
                realpath=os.readlink(path)
                result= '%s -> %s' % (os.path.basename(path), realpath)
            return result

        def ptree(startpath, depth=-1):
            ''' prints directory tree in 'tree' structure.

            Args:
                startpath: root path to start
                depth: depth of tree to print; default: -1 which signals not limit
            '''
            prefix=0
            if startpath != '/':
                if startpath.endswith('/'): startpath=startpath[:-1]
                prefix=len(startpath)
            for root, dirs, files in os.walk(startpath):
                level = root[prefix:].count(os.sep)
                if depth >-1 and level > depth: continue
                indent=subindent =''
                if level > 0:
                    indent = '|   ' * (level-1) + '|-- '
                subindent = '|   ' * (level) + '|-- '
                print('{}{}/'.format(indent, realname(root)))
                # print dir only if symbolic link; otherwise, will be printed as root
                for d in dirs:
                    if os.path.islink(os.path.join(root, d)):
                        print('{}{}'.format(subindent, realname(d, root=root)))
                for f in files:
                    print('{}{}'.format(subindent, realname(f, root=root)))


Command line Arguments
======================

    Command line arguments,

    .. code-block:: python

        if __name__ == '__main__':
            import argparse

            parser = argparse.ArgumentParser(description="""prints directory tree.""")
            parser.add_argument('--level', '-l', type=int, dest='depth', help='depth of tree to print')
            parser.add_argument('startpath', type=str, help='path to stating directory')
            args = parser.parse_args()
            argsd=vars(args)
            ptree(**argsd)

References
==========

ptree.py can be download from github_

.. _github: https://github.com/Acrisel/references/edit/master/osutils/ptree.py


Give us your feedback: support@acrisel.com
