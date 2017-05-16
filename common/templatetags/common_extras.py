from django import template
from django.contrib.auth.models import Group

register = template.Library()

# http://stackoverflow.com/questions/34571880/how-to-check-in-template-whether-user-belongs-to-group
@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    admin_group = Group.objects.get(name='admin')
    all_groups = user.groups.all()
    user_in_group = True if group in all_groups or admin_group in all_groups else False
    return user.is_superuser or user_in_group