# -*- coding: utf-8 -*-
"""
    extensions
    ~~~~~~~~~~

    This module contains flask extensions

    :copyright: (c) 2016 by Mehdy Khoshnoody.
    :license: GPLv3, see LICENSE for more details.
"""
{% if postgres %}
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
{% endif %}

exposed = []
{% if redis %}
from flask.ext.redis import FlaskRedis
{% endif %}

{% if postgres %}
db = SQLAlchemy()
exposed.append(db)

migrate = Migrate()
exposed.append(migrate)
{% endif %}

{% if redis %}
redis = FlaskRedis()
exposed.append(redis)
{% endif %}