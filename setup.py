"""
    This module
    
    :copyright: (c) 2016 by Mehdy Khoshnoody.
    :license: GPLv3, see LICENSE for more details.
"""

from distutils.core import setup

setup(
    name='flactory',
    version='0.1.0',
    py_modules=['flactory'],
    install_requires=[
        'click',
        'jinja2',
        'flask'
    ],
    data_files=[('flactory', 'templates/*.*')],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Code Generators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='flask project factory',
    entry_points='''
        [console_scripts]
        flactory=flactory:main
    ''',
    url='https://github.com/mehdy/flactory',
    license='GPLv3',
    author='mehdy',
    author_email='me@mehdy.net',
    description='A handy tool for creating and initializing flask applications'
)
