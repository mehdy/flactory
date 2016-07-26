# -*- coding: utf-8 -*-
"""
    .applications
    ~~~~~~
    
    This module
    
    :copyright: (c) 2016 by Mehdy Khoshnoody.
    :license: GPLv3, see LICENSE for more details.
"""
import json
import os
import re
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

import click

from flactory.utils import mkdirs, inside_dir


def check_name(ctx, param, value):
    """
        Checks the project name to be a valid name
    :param ctx: app context
    :param param: parameter
    :param value: the parameter value
    :return:
    """
    regex = re.compile('^[^0-9]\w*')
    if regex.match(value):
        return value
    while True:
        try:
            click.echo(
                click.style("{}".format(value), bold=True) +
                ' is not a valid python package name. try something else',
                err=True)
            value = param.prompt_for_value(ctx)
            if regex.match(value):
                return value
            continue
        except (KeyboardInterrupt, EOFError):
            raise ctx.Abort()


def check_template(ctx, _, value):
    """
        Checks the template to be valid template
    :param ctx: app context
    :param value: the parameter value
    :return:
    """
    if not value:
        # TODO: get list and show
        raise ctx.Abort()
    else:
        url = urlparse(value)
        if not url.netloc:
            url = url._replace(netloc='github.com')
        if url.path[-4:] == '.git':
            url = url._replace(path=url.path[:-4])
        path = os.path.join(os.environ['HOME'],
                            '.flactory/templates',
                            url.netloc, url.path)
        if os.path.isdir(path):
            return path
        # TODO: if not exist pull it automatically
        raise ctx.Abort()


@click.option('--template', '-t', type=click.STRING,
              callback=check_template,
              prompt="which template do you want to use")
@click.option('--name', '-n', type=click.STRING,
              callback=check_name,
              prompt="what's your project name")
@click.option('--version', '-v', type=click.STRING,
              default='0.1.0',
              prompt="what is your starting version")
@click.option('--destination', '-d', type=click.Path(),
              default='.',
              callback=lambda _, __, value: mkdirs(value, mode=0o755),
              prompt="where do you want to create your project")
def app(**kwargs):
    """
        Create applications with templates
    """
    template_dir = kwargs['template']
    destination = kwargs['destination']

    try:
        with open(os.path.join(template_dir, 'manifest.json')) as f:
            manifest = json.loads(f.read())
    except FileNotFoundError:
        # TODO: show error that template is invalid
        return click.Abort()

    state = manifest['state']
    for item in state:
        state[item]['value'] = click.prompt(state[item]['prompt'])

    # add other data to state
    state.update(**kwargs)

    entrypoint = os.path.join(template_dir, manifest['entrypoint'])
    for ctx, dirs, files in os.walk(entrypoint):
        with inside_dir(ctx.replace(entrypoint, destination)):
            for directory in dirs:
                if directory.startswith('$'):
                    directory = state[directory[1:]]
                mkdirs(directory, mode=0o755)

            for item in files:
                if item.startswith('$'):
                    item = state[item[1:]]
                with open(os.path.join(ctx, item)) as f:
                    template = Template(f.read())

                with open(item[:-4], 'w') as f:
                    f.write(template.render(**state))

    # now everything has been created TODO: be more verbose
