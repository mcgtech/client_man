# https://www.reddit.com/r/django/comments/4gkhye/how_to_split_modelspy_into_separate_files/
from .client import Client
from .interview import Interview, Qualification, Learning, PlannedTraining, OtherAgencies, OtherProgrammes
from .contract import Contract, TIOContract, ContractStatus

__all__ = ['Client', 'Contract', 'TIOContract', 'ContractStatus', 'Interview', 'Qualification', 'Learning', 'PlannedTraining', 'OtherAgencies', 'OtherProgrammes']