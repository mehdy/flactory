# -*- coding: utf-8 -*-
"""
    logger
    ~~~~~~

    This module contains logger utilities such as filters

    :copyright: (c) 2016 by Mehdy Khoshnoody.
    :license: GPLv3, see LICENSE for more details.
"""
import logging
from flask import request


class WebFilter(logging.Filter):
    """
        A filter that injects request information to a log record
    """

    def filter(self, record):
        """
            Injects information to log record
        :param record:
        """
        record.path = ''
        record.method = ''
        record.ip = ''
        record.user_agent = ''
        record.url = ''

        if request is not None:
            record.path = request.path
            record.url = request.url
            record.method = request.method
            record.ip = request.remote_addr
            record.user_agent = request.headers.get('user-agent', '')
        return True
