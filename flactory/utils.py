"""
    utils
    ~~~~~
    
    This module provides utility functions
    
    :copyright: (c) 2016 by Mehdy Khoshnoody.
    :license: GPLv3, see LICENSE for more details.
"""
import os
from contextlib import contextmanager


def mkdirs(path, mode=0o777):
    """
        creates directories recursively
    :param path: the path to create
    :param mode: directories permissions
    """
    head, tail = os.path.split(path)

    if head and not os.path.isdir(head):
        mkdirs(head, mode=mode)

    if not os.path.isdir(path):
        os.mkdir(path, mode)
    return path


@contextmanager
def inside_dir(path):
    """
        a context manager to run commands inside a directory
    :param path: the directory you want to run commands inside it.
    """
    old_path = os.path.abspath(os.curdir)
    os.chdir(path)
    yield
    os.chdir(old_path)
