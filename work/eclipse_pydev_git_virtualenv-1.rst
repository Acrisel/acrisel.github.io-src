:title: Team's Development Environment for Python Based Projects
:slug: eclipse-pydev-git-virtualenv
:date: 2017-11-03 20:47
:authors: Arnon Sela
:tags: Python, IDE, Virtualenv, Log, Distributed, Team

---------------------------------------------------
Development Environment for Python Projects: Part 1
---------------------------------------------------

Synopsis
========

For many years now we are using Eclipse with PyDev, git and Virtualenv. In time, our practices have been evolved and perfected. This inserts discuss our practical elements of a development environment and how to have them work together.

A development environment is composed from a few parts. In Python realm it would include:
    
    1. Python sensitive editor,
    #. Project directory structure reflected in filesystem, 
    #. Version and Change management,
    #. Sharing of code and data, 
    #. Testing faculty, and
    #. Packaging and distribution mechanisms.
    
This inserts would give a quick overview of the different parts. Consequence parts would give additional details on individual parts.  

Motivation
==========

Standardized structure of development environments has a few important benefits:

    1. Automation of tools to create and maintain environments can be developed and used.
    #. Once familiar with an environment, it is easy to transition and help with another. 
    
This article aims to be a corner stone on how to organize development projects in a pythonic way.
    
Keep in mind that development environment is a moving target. New and evolve development tools constantly require adaptation in development environment. Hence, any organization holding standards, needs to be able to quickly adopt changes giving room for new capabilities.

Overview
========

Lets get the rabbit out of the box, our common development environment includes:

    1. Eclipse IDE with PyDev (and additional plugins as needed).
    #. Git for version control and as repository for distributed development.
    #. Bugzilla for change control.
    #. *unittest* Python package to construct and run tests.
    #. *setuptools* and *twine* to publish via *pypi* repository (private or public) 
    
Our common projects file system structure is divided into a few parts:
     1. A Git repository that is located in a shared server accessed via SSH. 
     2. A personal coding area clone of the git repository. 
     3. A personal administration Eclipse's workspace; it is placed outside Git repository.
     4. Product area, used in case of compiled languages as the case in C/C++ and Java. Note, if product area is part of code area, .gitignore should include product elements that should not be uploaded into Git repository. 


Filesystem
==========

Major folder areas are admin, source, data, work, and log areas. In multi-projects environment this will look as follows:

    .. code:: python
        :number-lines:
     
         /var/home/user-name/division-name (or any other path that represent specific group)
         |-- /sand
         |   |-- project-name
         |   |   |-- project folders (see next diagram)
         |-- /admin
         |   |-- workspace-name
         |-- /log (may be link to /var/log)
         |   |-- project-name
         |-- /data
         |   |-- long term data folders and files
         |-- /work
         |   |-- temporary work areas for running programs
         |-- /run
         |   |-- in case programs needs to have artifacts that represent a running program
         |-- /venv
         |   |-- private project based python virtualenvs
         
         /var
         |-- /venv 
         |   |-- common project based python virtualenvs

A common Eclipse project's source code folder will look as follows:

    .. code:: python
        :number-lines:

         /path/to/sand
         |-- project-name
         |   |-- branch-id (e.i, master (next version) or a version branch)
         |   |   |-- .git
         |   |   |-- .gitignore
         |   |   |-- project-name (i.e., python deployment package)
         |   |   |   |-- __init__.py
         |   |   |   |-- bin (python command-line and GUI programs)
         |   |   |   |-- config (configuration file or package for dev, test, prod)
         |   |   |   |-- lib (python program with class and function definitions)
         |   |   |   |-- src (Compiled languages source)
         |   |   |   |-- static (reference data folders and files)
         |   |   |-- tests
         |   |   |   |-- main_test_program.py
         |   |   |   |-- test-packages-and-programs(.py)
         |   |   |-- examples
         |   |   |   |-- example-packages-and-programs(.py)
         |   |   |-- docs
         |   |   |   |-- documentation
         |   |   |-- products (C++/Java)
         |   |   |   |-- lib (e.g., .a and .jar libraries)
         |   |   |   |-- bin (exec - link products)
         |   |   |   |-- out (.o/.class - compile products)
         |   |   |-- AUTHORS.txt
         |   |   |-- CHANGES.txt
         |   |   |-- LICENSE.txt
         |   |   |-- README.rst
         |   |   |-- setup.py

Editor
======

The most simplistic environment would include editor and Python interpreter. This is would suffice small projects. When dealing with large projects with a few file each, it is important to have capabilities to do more than just edit a file and run the program written in it.

We use Eclipse with PyDev as IDE for Python projects. There are many benefits for using Eclipse, just to name a few:

    1. Search over the complete workspace.
    #. Multiple project is a single view.
    #. Running programs is a only a button a way.

Plus, it 

    1. Facilitates other programming languages.
    #. Integrates with git and Bugzilla (or other change control)
    #. Integrates with Python's Virtualenv.

Tips
----

Create PyDev Project
~~~~~~~~~~~~~~~~~~~~

In our projects we split between Eclipse's workspace definitions and projects included in a workspace.  Workspace is places in admin

Choose Python from the virtualenv of the project.

Code Style
~~~~~~~~~~

PyDev can be set to check PEP8 coding style compliance (PyDev -> Editors -> Code Analysis). Turn it on to make sure your coding style matches PEP8.

Profiling
~~~~~~~~~
    
There are several tools that can be use to profile Python program. PyDev include hooks to PyVmMonitor, which enables profiling of python program directly from Eclipse. PyVmMonitor needs to be installed on your development computer (laptop).

Virtualenv
~~~~~~~~~~

When you create PyDev project, it needs to be linked with Python interpreter. Choose Python interpreter from the virtualenv of the project.

