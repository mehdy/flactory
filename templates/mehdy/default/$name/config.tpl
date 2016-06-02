# -*- coding: utf-8 -*-
"""
    config
    ~~~~~~

    This module contains configuration classes for the application

    :copyright: (c) 2016 by Mehdy Khoshnoody.
    :license: GPLv3, see LICENSE for more details.
"""
import os


class Config(object):
    """
        Default configuration class
    """
    DEPLOYMENT = False
    TESTING = False
    DEBUG = False

    NAME = {{ name }}
    VERSION = {{ version }}

    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-mode-secret-key')

    # media folders and urls
    DATA_FOLDER = '{{ data_folder }}'
    DATA_URL = '{{ data_url }}'

    INSTALLED_PLUGINS = ()

    {% if redis %}
    REDIS_URL = "redis://{}:6379/0".format(os.environ.get('REDIS_HOSTNAME'))
    REDIS_PREFIX = "{{ name }}:"
    {% endif %}

    {% if postgres %}
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:5432/{{ postgres_db }}'.format(
        os.environ.get('PG_USERNAME'),
        os.environ.get('PG_PASSWORD'),
        os.environ.get('PG_HOSTNAME'))
    {% endif %}

    LOG_FORMAT = ('\033[1;39m' + '=' * 50 +
                  '\n\033[1;35m[%(asctime)s]\033[1;m \033[1;32m[%(name)s] '
                  '\033[1;31m[%(levelname)s] '
                  '\033[1;36m[%(pathname)s:%(lineno)d]\n\033[1;37m[%(ip)s] '
                  '\033[1;34m[%(method)s %(url)s]\n'
                  '\033[1;38m[%(user_agent)s]\n\033[1;39m'
                  '\n#\033[1;39m %(message)s\n' + '-' * 50 + '\033[1;m')


class Development(Config):
    """
        Development configuration class
    """

    DEBUG = True

    LOG_PATH = {{ dev_log_path }}
    DEBUG_LOG = os.path.join(LOG_PATH, "debug.log")
    ERROR_LOG = os.path.join(LOG_PATH, "error.log")


class DeploymentConfig(DefaultConfig):
    """
        Deployment configuration class
    """
    DEBUG = False
    DEPLOYMENT = True

    LOG_PATH = {{ dep_log_path }}
    DEBUG_LOG = os.path.join(LOG_PATH, "debug.log")
    ERROR_LOG = os.path.join(LOG_PATH, "error.log")

