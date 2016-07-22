"""
    main
    ~~~~
    
    This module creates the cli application and implements general commands
    
    :copyright: (c) 2016 by Mehdy Khoshnoody.
    :license: GPLv3, see LICENSE for more details.
"""

import click


@click.group()
@click.version_option()
@click.help_option()
def main():
    """
        Flactory makes creating large flask application easier
    """
    pass
