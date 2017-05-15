from django.apps import AppConfig
from django.db.models.signals import post_save
from .models import Person
from client_man.client.signals import create_address


class ClientConfig(AppConfig):
    name = 'client'
    def ready(self):
        post_save.connect(create_address, sender=Person)
