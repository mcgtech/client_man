from django.contrib import admin
from .models import Client, Contract, ContractStatus
from common.models import Person, Note, Address, Telephone

admin.site.register(Person)
admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(ContractStatus)
admin.site.register(Note)
admin.site.register(Address)
admin.site.register(Telephone)