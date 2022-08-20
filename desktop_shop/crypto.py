# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 20:19:46 2020

@author: Korean_Crimson
"""
from dataclasses import dataclass
import enum
import hashlib
import random
import secrets
from typing import Callable, Dict, Optional

HashFunctionCallable = Callable[[str, str, int], str]
BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


class InvalidHashFunctionException(ValueError):
    """Exception thrown when an invalid hash function is specified"""


class HashFunctions(enum.Enum):
    """hash functions enum (values are functions)"""

    HASHLIB_PBKDF2_HMAC_SHA256 = enum.auto()


@dataclass
class HashFunction:
    """Contains a hash function enum and its iterations keyword.
    Encapsulates a hash operation.
    """

    function: HashFunctions
    iterations: int

    def hash(self, password: str, salt: str) -> str:
        """Returns the result of the hash function hashing the provided password and salt"""
        function = get_function_from_hash_function_enum(self.function)
        return function(password, salt, self.iterations)

    def __str__(self):
        return f"{self.function.name}::{self.iterations}"


def hash_string(password: str, salt: str, iterations: int = 100_000) -> str:
    """Hashes the specified password with the passed salt.
    Returns hash in hex format (str).
    """
    encoded_password = bytes(password, encoding="utf-8")
    encoded_salt = bytes(salt, encoding="utf-8")
    derived_key = hashlib.pbkdf2_hmac(
        "sha256", encoded_password, encoded_salt, iterations=iterations
    )
    return derived_key.hex()


def get_hash_function(iterations: int) -> HashFunction:
    """Returns a HashFunction object"""
    return HashFunction(function=HashFunctions.HASHLIB_PBKDF2_HMAC_SHA256, iterations=iterations)


def get_hash_function_from_string(hash_function_name: str) -> Optional[HashFunction]:
    """Looks up a hash function in the HashFunctions enum from a str key in
    the format name::iterations.
    """
    name, iterations = hash_function_name.split("::")
    hash_function = HashFunctions.__dict__.get(name)
    if hash_function is not None:
        return HashFunction(function=hash_function, iterations=int(iterations))
    return None


def get_function_from_hash_function_enum(
    hash_function: HashFunctions,
) -> HashFunctionCallable:
    """Looks up the passed HashFunctions enum and returns a corresponding function handle"""
    functions: Dict[HashFunctions, HashFunctionCallable] = {
        HashFunctions.HASHLIB_PBKDF2_HMAC_SHA256: hash_string
    }
    hash_function_callable = functions.get(hash_function)
    if hash_function_callable is None:
        raise InvalidHashFunctionException("Hash function could not be found!")
    return hash_function_callable


def generate_new_salt() -> str:
    """Generates a new base 62 encoded salt based on a cryptographically
    secure random number, to hash strings.
    """
    rng = random.SystemRandom()
    random_number = rng.randint(0, 2**64)
    salt = _b62encode(random_number)
    return salt


def _b62encode(num: int, alphabet: str = BASE62) -> str:
    """Encode a positive number into Base 62 and return the string."""
    char_array = [] if num else [alphabet[0]]
    base = len(alphabet)
    while num:
        num, rem = divmod(num, base)
        char_array.append(alphabet[rem])
    char_array.reverse()
    encoded_string = "".join(char_array)
    return encoded_string


def generate_new_session_id() -> str:
    """Creates a cryptographically-secure, URL-safe string"""
    return secrets.token_urlsafe(16)
