:title: Python Enhancement Proposal for Configuration Parameters
:slug: PEP-configuration-parameters
:date: 2017-11-09 20:47
:authors: Arnon Sela
:tags: Python, project, parameters

---------------------------------------------------
Development Environment for Python Projects: Part 2
---------------------------------------------------

Synopsis
========

Project configuration parameters have a few dimensions (e.g, users, hosts, development, test, and production). Managing these dimensions in a project is an art. As part of standard Python environments we introduce parametric evaluation for YAML configuration. The key features are:

    1. configuration chaining.
    #. value evaluation and expansion.
    #. integration with virtualenv.
    #. integration with environment variables.
    #. managed-configuration with user and api interfaces.
    
With these features, projects can manage their parameters and form better cooperation with other projects.

Motivation
==========

Software products may have many parameters to that would direct their behavior in varies situations. Project may use other project themselves have their own configuration. 

We wanted a way to manage project configuration parameters. Same as Virtualenv manages environments in respect to what packages are installed in them. 

Overview
========

Project configuration parameters have a few dimensions (e.g, ). A project may wish to differentiate among developments, tests, and production environments. There may be need for personalization of environment to suite personal environments. There may also be different settings for specialized deployments on specific hosts (for specialized purpose, for different operating systems, and different installations). Yet another dimension is the versions for the projects which most probably will have different parameters.

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

