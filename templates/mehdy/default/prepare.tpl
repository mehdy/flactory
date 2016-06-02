#!/bin/bash

pip install -r requirements.txt

{% if postgres %}
export PG_HOSTNAME=postgres
export PG_USERNAME={{ postgres_user }}
export PG_PASSWORD={{ postgres_pass }}
{% endif %}
{% if redis %}
export REDIS_HOSTNAME=redis
{% endif %}