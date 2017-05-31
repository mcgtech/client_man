from django import template
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from django.conf import settings

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


@register.filter(name='get_partner_logo')
def get_partner_logo(user):
    logo = None
    if has_group(user, settings.HI_COUNCIL_PART):
        logo = 'high_council_logo.png'
    elif has_group(user, settings.RAG_TAG_PART):
        logo = 'rag_tag_logo.png.png'
    if logo is not None:
        logo = '<img src="/static/img/' + logo + '"/>'
    return mark_safe(logo)