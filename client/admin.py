from django.contrib import admin
from .models import Client, Contract, TIOContract, ContractStatus, Interview
from common.models import Person, Note, Address, Telephone

admin.site.register(Person)
admin.site.register(Client)
admin.site.register(Interview)
admin.site.register(Contract)
admin.site.register(TIOContract)
admin.site.register(ContractStatus)
admin.site.register(Note)
admin.site.register(Address)
admin.site.register(Telephone)