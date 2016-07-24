"""
    repository
    ~~~~~~~~~~
    
    This module manages the templates repositories
    
    :copyright: (c) 2016 by Mehdy Khoshnoody.
    :license: GPLv3, see LICENSE for more details.
"""
import os
import subprocess
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


import click

from flactory.utils import mkdirs, inside_dir


def check_repo(_, __, value):
    # checks if the value is a valid url or not
    url = urlparse(value)
    if not url.scheme:
        url = url._replace(scheme='https')
    if not url.netloc:
        url = url._replace(netloc='github.com')
    if url.path[-4:] != '.git':
        url = url._replace(path=url.path + '.git')
    return url


@click.argument('repo', nargs=1, callback=check_repo)
def pull(**kwargs):
    """
        pull application templates

        all templates will be pulled and saved inside $HOME/.flactory/templates
    """
    repo = kwargs['repo']
    templates_path = os.path.join(os.environ['HOME'], '.flactory/templates')
    template_path = os.path.join(templates_path,
                                 kwargs['repo'].netloc,
                                 kwargs['repo'].path[:-4])
    repr_name = click.style("[{}] {}".format(repo.netloc, repo.path[:-4]),
                            bold=True)
    mkdirs(templates_path, mode=0o755)

    if os.path.isdir(template_path):
        click.echo(repr_name + " exists! trying to update it...")
        with inside_dir(template_path):
            res = subprocess.Popen(['git pull'],
                                   stderr=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   shell=True)
    else:
        click.echo(
            "couldn't find " + repr_name + " locally! trying to pull it...")
        mkdirs(template_path, mode=0o755)
        with inside_dir(template_path):
            res = subprocess.Popen(
                ['git clone ' + kwargs['repo'].geturl() + ' .'],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                shell=True)

    if res.wait() == 0:
        click.echo(click.style(
            repr_name + " has been pulled successfully!", fg='green'))
    else:
        click.echo(click.style(
            "couldn't pull " + repr_name + " due to: {}".format(
                res.stderr.read().decode()), fg='red'))
