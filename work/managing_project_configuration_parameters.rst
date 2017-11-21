:title: Managing Project Configuration Parameters
:slug: python-project-configuration-parameters
:date: 2017-11-03 20:47
:authors: Arnon Sela
:tags: Python, project, configuration, parameters

----------------------------------------------------
Managed Configuration Parameters for Python Projects
----------------------------------------------------

Synopsis
========

Project configuration parameters have a few dimensions (e.g, users, hosts, development, test, and production). Managing these dimensions in a project is an art. Additional complexity is introduced when using other packages having their own configuration parameters. 

This PEP is to enable Python packages (projects) to create a single configuration parameters mechanism. Configuration parameters in package lifecycle includes multiple dimensions:

    1. installation environments: research, development, test, and production.
    #. multi packages configuration hierarchy.
    #. multi level personalization (e.g., user, group, host, and cluster).

The key features needed are:

    1. configuration chaining (include).
    #. value evaluation and expansion (including value referencing).
    #. personalization.
    #. integration with setup tools for binding install values.
    #. managed-configuration with user and api interfaces.
    #. integration with virtualenv and environment variables.
    
With these features, projects can manage their parameters and form better cooperation with packages they use, or packages using them.

Motivation
==========

It is common that software products may have many parameters that would direct their behavior in varies situations. Example for project configuration parameters include:

    1. Logging configuration.
    #. Ports for communication in distributed environment.
    #. Directories and file patterns to create and use.
    #. Processing or threading definitions.

Project may use other projects having their own configuration parameters. This creates a complicated configuration parameters environment where one need to maintain in multiple configuration files. This is made more complicated when one projects uses multiple Python frameworks each with its own configuration mechanism.

For example, package A uses package B to create files it can then uses.  Package B preprocessing of the data acquires temporary folders which can be set in its configuration $HOME/A.conf. Package B has it own configuration for database login parameters and temporary folders in similar configuration $HOME/B.conf. To use package B, one need to maintain two configuration files. 

We wanted a way to manage project configuration parameters. Same as Virtualenv manages environments in respect to packages that are installed in them. Configenv would create a mechanism for packages to have single configuration for their parameters. 


Setting stage
=============

Here is an example use of configenv.

    .. code:: python
         :number-lines:
     
         from configenv import configenv as cenv
         import logging
         
         # load configuration for package
         package_name = os.path.basename(os.path.dirname(__file__))
         package_config = cenv.load(root = package_name)
         
         # loading and setting logging configuration 
         logging.config.dictConfig(cenv.load(root = 'logging'))
         
In this example, a single configuration file include logging configuration as well as the particular package configuration. Line 6 and 9 load package and logging configuration respectively.

Configuration chain
===================

Project dimensions builds a chain of configurations. Each link in the chain is a configuration file overriding parameters to its predecessor. Depending on the dimension, configuration files can also be add parameter.

example for configuration chain:

    ..code:: python
        :number-lines:
    
        /usr/local/share/virtualenvs/projectname/lib/python3.6/somepackage/somepackage.conf
        /home/me/.packagename.conf
        
        
        

         

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

