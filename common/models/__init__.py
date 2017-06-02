# https://www.reddit.com/r/django/comments/4gkhye/how_to_split_modelspy_into_separate_files/
from .auditable import Auditable
from .person import Address, Person, Telephone, Note

__all__ = ['Auditable', 'Address', 'Note', 'Person', 'Telephone']