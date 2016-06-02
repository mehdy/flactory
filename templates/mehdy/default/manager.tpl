#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    manager
    ~~~~~~~

    This module provides some basic commands for managing the project via
    command line.

    :copyright: (c) 2016 by Mehdy Khoshnoody.
    :license: GPLv3, see LICENSE for more details.
"""
from flask.ext.script import Manager, prompt_bool

from {{ name }}.factory import create_app
{% if postgres %}
from flask.ext.migrate import MigrateCommand
from {{ name }}.extensions import db
{% endif %}

manager = Manager(create_pp)
manager.add_option('-c', '--config', dest='config', required=False)

{% if postgres %}
manager.add_command('db', MigrateCommand)

@manager.command
def create_all():
    """Creates database tables"""
    db.create_all()


@manager.command
def drop_all():
    """Drops all database tables"""

    if prompt_bool("Are you sure? You will lose all your data!"):
        db.drop_all()
{% endif %}

@manager.shell
def make_shell_context():
    return dict(app=app{% if postgres %}, db=db{% endif %})

if __name__ == "__main__":
    manager.run()
