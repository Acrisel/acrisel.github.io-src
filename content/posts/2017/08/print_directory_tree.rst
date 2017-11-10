:title: Python Print Directory Tree
:slug: python-print-directory-tree
:date: 2017-08-09 23:01:44
:athuors: Arnon Sela
:tags: OS, Utilities, Directory, Tree, Linux, Unix, Python

----------------------------
Mimicking Linux Tree Utility
----------------------------

Introduction
============

Many blogs are showing how to print directory tree using Python.
Drawing from those examples, we built our version.  The primary drivers were:

    1. Compatibility with Python3
    2. Print symbolic links
    3. Limit depth of tree

    Example output:

    .. code-block:: python

        $ ptree.py -l 2 /var

        var -> private/var/
        |-- venv -> /usr/local/share/virtualenvs
        |-- accord/
        |   |-- .DS_Store
        |   |-- data/
        |   |   |-- .DS_Store
        |-- acrisel/
        |   |-- .DS_Store
        |   |-- .gitignore
        |   |-- accord/
        |   |   |-- .DS_Store

Function Code
=============

    .. code-block:: python

        import os

        def realname(path, root=None):
            if root is not None:
                path=os.path.join(root, path)
            result=os.path.basename(path)
            if os.path.islink(path):
                realpath=os.readlink(path)
                result= '%s -> %s' % (os.path.basename(path), realpath)
            return result

        def ptree(startpath, depth=-1):
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

I will refrain from going over the code, otherwise self-explanatory,  except mentioning the following:

    1. os.walk treats symbolic links per their target.  Therefore, a symbolic link may appear in dirs and files.
    2. only two main features of *tree* are replicated:  accepting both a root path and depth to explore.


Command line Arguments
======================

Command line arguments is simple and self explanatory ...

    .. code-block:: python

        if __name__ == '__main__':
            import argparse

            parser = argparse.ArgumentParser(description='prints directory tree.')
            parser.add_argument('--level', '-l', type=int, dest='depth', default=-1,
                                help='depth of tree to print')
            parser.add_argument('startpath', type=str,
                                help='path to stating directory')
            args = parser.parse_args()
            argsd=vars(args)
            ptree(**argsd)

References
==========

ptree.py can be download from github_

.. _github: https://github.com/Acrisel/references/edit/master/osutils/ptree.py


| Give us your feedback: support@acrisel.com
| Visit us at our home_

.. _home: http://www.acrisel.com
