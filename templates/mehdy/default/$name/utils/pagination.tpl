# -*- coding: utf-8 -*-
"""
    pagination
    ~~~~~~~~~~

    This module provides some functions to paginate anything

    :copyright: (c) 2016 by Mehdy Khoshnoody.
    :license: GPLv3, see LICENSE for more details.
"""
import functools
from flask import request, url_for, jsonify


def sql_paginate(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        query = f(*args, **kwargs)

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 25, type=int)

        p = query.paginate(page, per_page)

        meta = {'page': page, 'per_page': per_page,
                'total': p.total, 'pages': p.pages}

        if p.has_prev:
            meta['prev_url'] = url_for(request.endpoint, page=p.prev_num,
                                       per_page=per_page, _external=True,
                                       **kwargs)
        else:
            meta['prev_url'] = None

        if p.has_next:
            meta['next_url'] = url_for(request.endpoint, page=p.next_num,
                                       per_page=per_page, _external=True,
                                       **kwargs)
        else:
            meta['next_url'] = None

        meta['first_url'] = url_for(request.endpoint, page=1,
                                    per_page=per_page, _external=True,
                                    **kwargs)
        meta['last_url'] = url_for(request.endpoint, page=p.pages,
                                   per_page=per_page, _external=True,
                                   **kwargs)

        results = [item.to_dict() for item in p.items]

        return jsonify({'news': results, 'meta': meta})
    return wrapped

