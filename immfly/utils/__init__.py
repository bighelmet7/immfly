"""
Common utilities for the project.
"""

from random import choices
from string import ascii_uppercase


def random_letters(n_letters: int = 1) -> str:
    """
    random_letters returns N random letters from string.ascii_uppercase.
    """
    return ''.join(choices(ascii_uppercase, k=n_letters))
