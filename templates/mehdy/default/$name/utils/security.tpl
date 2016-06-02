# -*- coding: utf-8 -*-
"""
    security
    ~~~~~~~~

    This module provides some functions to encode, decode and other security
     stuffs

    :copyright: (c) 2016 by Mehdy Khoshnoody.
    :license: GPLv3, see LICENSE for more details.
"""
import functools
import os
import random
import string
from base64 import b64decode, b64encode
from hashlib import sha512


def _generate_password_hash(password, salt):
    """
        Hashes the given password with given salt with SHA-512
    :param password: password to hash
    :type password: bytes
    :param salt: salt to make the password salty
    :type salt: bytes
    :returns: a random salty hashed password
    :rtype: bytes
    """

    sha = sha512(password)
    sha.update(salt)

    return sha.digest()


def encode_hash(password, salt_length=8):
    """
        Retrieves a series of random characters from /dev/urandom with a
        length of given salt_length
    :param password: password to hash
    :type password: str
    :param salt_length: length of salt
    :type salt_length: int
    :return: an encoded salty hashed password
    :rtype: str
    """

    salt = os.urandom(salt_length)
    hashed = _generate_password_hash(password.encode(), salt)
    encoded_hash = b64encode(hashed + salt).decode()

    return encoded_hash


def check_password_hash(encoded_hash, password):
    """
        Verifies matching given password and an encoded hash
    :param encoded_hash: the encoded hash to check with
    :type encoded_hash: str
    :param password: user given password
    :type password: str
    :return: state of password matching
    :rtype: bool
    """

    decoded_hash = b64decode(encoded_hash)
    hash_digest, salt = decoded_hash[:64], decoded_hash[64:]

    return _generate_password_hash(password.encode(), salt) == hash_digest


def generate_random_token(length):
    """
        Generates a unique random alphanumeric string with the given length
    :param length: length of token
    :type length: int
    :return: a unique random alphanumeric string
    :rtype: str
    """
    return ''.join(random.SystemRandom().choice(
        string.ascii_lowercase + string.digits) for _ in range(length))

