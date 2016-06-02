# -*- coding: utf-8 -*-
"""
    factory
    ~~~~~~~

    This module provides some functions to create and configure a flask app

    :copyright: (c) 2016 by Mehdy Khoshnoody.
    :license: GPLv3, see LICENSE for more details.
"""
import logging
import logging.handlers

from flask import Flask, g, request

import extensions
from .models import Person
from .utils.logger import WebFilter

__all__ = ['create_app']


def create_app(config):
    """
        Creates a flask application and configure it's blueprints,
        extensions and etc.
    :return: a flask application
    """
    app = Flask("{{name}}")

    app.config.from_object(config)

    configure_logger(app)

    configure_extensions(app)

    register_blueprints(app)

    return app


def configure_logger(app):
    """
        Configures the logger and registers the logger handlers.
    :param app: the flask application
    """
    app.logger.addFilter(WebFilter())
    formatter = logging.Formatter(app.config['LOG_FORMAT'])

    debug_file_handler = logging.handlers.TimedRotatingFileHandler(
        app.config['DEBUG_LOG'], when='D', backupCount=10)

    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(formatter)
    app.logger.addHandler(debug_file_handler)

    error_file_handler = logging.handlers.TimedRotatingFileHandler(
        app.config['ERROR_LOG'], when='D', backupCount=10)

    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)


def register_blueprints(app):
    """
        Registers the blueprints on the application.
    :param app: the flask application
    """
    blueprints = app.config['INSTALLED_BLUEPRINTS']
    for blueprint_name in blueprints:
        try:
            bp = __import__(
                '{{name}}.plugins.{0}'.format(blueprint_name),
                fromlist=[blueprint_name])
            app.register_blueprint(bp.controller)
        except ImportError:
            app.logger.warning("couldn't register {} blueprint".format(
                blueprint_name
            ))


def configure_extensions(app):
    """
        Registers the extensions on the application.
    :param app: the flask application
    """
    for ext in extensions.exposed:
        ext.init_app(app)
