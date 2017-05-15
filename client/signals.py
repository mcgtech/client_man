from .models import Address

# whene a person model is created, associate an empty address with it
def create_address(sender, **kwargs):
    print('xxx');
    if kwargs["created"]:
        person_instance = kwargs["instance"]
        address = Address(person=person_instance)
        address.save()
