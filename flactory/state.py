"""
    state
    ~~~~~
    
    This module handles the template state and how it should be changed
    
    :copyright: (c) 2016 by Mehdy Khoshnoody.
    :license: GPLv3, see LICENSE for more details.
"""
import click

types = {
    'int': int,
    'bool': bool,
    'str': str,
    None: None
}


def parse_manifest(manifest):
    state = dict(sorted(
        manifest['state'].items(),
        key=lambda i: i[1].get('id', 0),
        reverse=True))
    excludes = dict(sorted(
        manifest['excludes'].items(),
        key=lambda i: i[1].get('id', 0),
        reverse=True))
    excluded_files = []
    excluded_dirs = []

    for item in excludes:
        if not click.confirm(item['prompt'], default=True, prompt_suffix=' '):
            if item['type'] == 'file':
                excluded_files.append(item['value'])
            else:
                excluded_dirs.append(item['value'])

    # TODO: handle states which are related to excludes
    for item in state:
        if state[item]['type'] == 'confirm':
            state[item]['value'] = click.confirm(
                state[item]['prompt'],
                default=state[item].get('value', False),
                prompt_suffix=' '
            )
        else:
            state[item]['value'] = click.prompt(
                state[item]['prompt'],
                default=state[item].get('value'),
                type=types[state[item].get('type')],
                prompt_suffix=' '
            )

            # TODO: handle other related states
    return state, excluded_dirs, excluded_files
