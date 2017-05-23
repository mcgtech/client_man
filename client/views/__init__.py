# https://stackoverflow.com/questions/1921771/django-split-views-py-in-several-files
# https://stackoverflow.com/questions/20010991/split-views-py-into-multiple-files
from .client.client_crud import *
from .contract.contract_crud import *
from .client.client_searching import *
from .migration.migration import *