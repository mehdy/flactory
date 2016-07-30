.. _getting-started:

Getting Started
===============

.. _installation:

Installation
------------

it's as easy as installing any other python packages. just make sure you've
installed pip properly and execute to install or upgrade it::

    $ pip install -U flactory

Create your first App
---------------------

flactory uses templates to generate application code bases. you can create
and use your own template. but for the purpose of this document we'll be
using `Flarge <https://github.com/mehdy/flarge>`_ ! a template which I
created for my own applications.

So first of all we need to get the template to be available to use.
In order to do that run::

	$ flactory pull mehdy/flarge

And you should see this::

	couldn't find [github.com] mehdy/flarge locally! trying to pull it...
	[github.com] mehdy/flarge has been pulled successfully!

It means flactory has pulled the template (via git) and now it's available to
use.

Now for creating an application from this template just run::

	$ flactory create app

it will ask you to select the template you want, so answer it with ``mehdy/flarge``::

	which template do you want to use: mehdy/flarge

and then it will ask you some other questions like the name and version of
your project and the path you want the project to be created in. answer the
questions and it'll create and configure you your project from the template.
