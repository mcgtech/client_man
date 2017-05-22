# https://stackoverflow.com/questions/1921771/django-split-views-py-in-several-files
# https://stackoverflow.com/questions/20010991/split-views-py-into-multiple-files
from views_client_details import home_page, quick_client_search, client_search, client_detail, client_new, client_edit
from views_migration import load_clients