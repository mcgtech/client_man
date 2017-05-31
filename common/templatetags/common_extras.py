from django import template
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

register = template.Library()

# http://stackoverflow.com/questions/34571880/how-to-check-in-template-whether-user-belongs-to-group
@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    admin_group = Group.objects.get(name='admin')
    all_groups = user.groups.all()
    user_in_group = True if group in all_groups or admin_group in all_groups else False
    return user.is_superuser or user_in_group

@register.filter(name='render_checkbox')
def render_checkbox(checked):
    icon = 'glyphicon-ok' if checked else 'glyphicon-remove'
    return mark_safe('<span class="glyphicon ' + icon + '"></span>')