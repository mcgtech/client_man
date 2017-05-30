# https://www.reddit.com/r/django/comments/4gkhye/how_to_split_modelspy_into_separate_files/
from .auditable import Auditable
from .note import Note
from .person import Address, Person, Telephone
from .html_template import *

__all__ = ['Auditable', 'Note', 'Address', 'Person', 'Telephone']