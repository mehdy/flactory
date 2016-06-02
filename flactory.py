"""
    flactory
    ~~~~~~~~
    
    This module creates and run the click app
    
    :copyright: (c) 2016 by Mehdy Khoshnoody.
    :license: GPLv3, see LICENSE for more details.
"""
import json
import os
import re

import click
import click.termui
import pkg_resources as res
from jinja2 import Template


def check_path(ctx, param, value):
    """
        Checks the path to see if it's a valid path and makes sure it is
        empty or it hasn't been created yet
    :param ctx: app context
    :param param: parameter
    :param value: the parameter value
    :return:
    """
    while True:
        try:
            if os.path.isfile(value):
                click.echo(
                    '"{}" is a file. you must enter a path'.format(value),
                    err=True)
            elif os.path.exists(value):
                if os.listdir(value):
                    if click.confirm(
                            '"{}" exists and it is not empty. '
                            'do you want to continue?'.format(value)):
                        break
                else:
                    break
            else:
                break
            value = param.prompt_for_value(ctx)
            continue
        except (KeyboardInterrupt, EOFError):
            raise click.Abort()
    return value


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
                '"{}" is not a valid python package name. '
                'try something else'.format(value),
                err=True)
            value = param.prompt_for_value(ctx)
            if regex.match(value):
                return value
            continue
        except (KeyboardInterrupt, EOFError):
            raise click.Abort()


def check_template(ctx, param, value):
    """
        Checks the template to be valid template
    :param ctx: app context
    :param param: parameter
    :param value: the parameter value
    :return:
    """
    while True:
        try:
            user, template = value.split('/')
            if user in res.resource_listdir('flactory', 'templates'):
                if template in res.resource_listdir('flactory',
                                                    'templates/' + user):
                    return value
                click.echo('"{}" does not have a template named "{}"'.format(
                    user, value),
                    err=True)
            else:
                click.echo('user "{}" does not exist'.format(user), err=True)
            value = param.prompt_for_value(ctx)
            continue
        except (KeyboardInterrupt, EOFError):
            raise click.Abort()


@click.group()
def main():
    """
        Flactory helps you to create flask application
    :return:
    """
    pass


@main.command()
@click.option('--template', '-t', type=click.STRING,
              default="mehdy/default",
              callback=check_template,
              prompt="which template do you want to use")
@click.option('--name', '-n', type=click.STRING,
              callback=check_name,
              prompt="what's your project name")
@click.option('--version', '-v', type=click.STRING,
              default='0.1.0',
              prompt="what is your starting version")
@click.option('--vagrant', '-v', is_flag=True, default=True,
              prompt="would you like to use vagrant?")
@click.option('--docker', is_flag=True, default=True,
              prompt="would you like to use docker")
@click.option('--postgres', '-p', is_flag=True, default=True,
              prompt="would you like to use postgres")
@click.option('--postgres-db', type=click.STRING,
              prompt="what's your postgres db name")
@click.option('--postgres-user', type=click.STRING,
              prompt="what's your postgres db username")
@click.option('--postgres-pass', type=click.STRING,
              prompt="what's your postgres db password")
@click.option('--redis', '-r', is_flag=True, default=True,
              prompt="would you like to use redis")
@click.option('--destination', '-d', type=click.Path(),
              default='.',
              callback=check_path,
              prompt="where do you want to create your project")
@click.option('--data-dir', type=click.Path(),
              default='data',
              callback=check_path,
              prompt="where do you want to store your data")
@click.option('--data-url', type=click.Path(),
              default='/data/',
              prompt="where you you want to expose your data")
@click.option('--dev-log-path', type=click.Path(),
              default='logs',
              callback=check_path,
              prompt="where do you want to store your logs(dev mode)")
@click.option('--dep-log-path', type=click.Path(),
              default='logs',
              callback=check_path,
              prompt="where do you want to store your logs(dep mode)")
def new(**kwargs):
    """
        Create a new application
    """
    template_dir = os.path.join('templates', kwargs['template'])
    manifest = json.loads(
        res.resource_string(
            'flactory', os.path.join(template_dir, 'manifest.json')).decode())

    def process(root_template, ctx):
        """
            process the creating files and directories
        :param root_template: the template root path
        :param ctx: the directory context
        """
        click.echo(ctx)
        for file in ctx['files']:
            template = Template(
                res.resource_string(
                    'flactory',
                    os.path.join(
                        root_template,
                        os.path.splitext(file)[0] + '.tpl')).decode())

            with open(file, 'w') as f:
                f.write(template.render(**kwargs))

        root = os.path.abspath('.')
        for directory in ctx['directories']:
            dir_name = kwargs[directory['name'][1:]] if directory[
                'name'].startswith('$') else directory['name']
            os.mkdir(dir_name)
            os.chdir(os.path.join(root, dir_name))
            process(os.path.join(root_template, directory['name']),
                    directory['tree'])
            os.chdir(root)

    if not os.path.exists(kwargs['destination']):
        os.mkdir(kwargs['destination'])
    os.chdir(kwargs['destination'])
    process(template_dir, manifest['tree'])


if __name__ == '__main__':
    main()
