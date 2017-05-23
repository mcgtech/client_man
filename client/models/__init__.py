# https://www.reddit.com/r/django/comments/4gkhye/how_to_split_modelspy_into_separate_files/
from .client import Client
from .contract import Contract

__all__ = ['Client', 'Contract']