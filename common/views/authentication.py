from django.conf import settings

def admin_user(user):
    return user.is_superuser or user.groups.filter(name=settings.ADMIN_GROUP).exists()

def job_coach_man_user(user):
    return admin_user(user) or user.groups.filter(name=settings.JOB_COACH_MAN).exists()

def job_coach_user(user):
    return job_coach_man_user(user) or user.groups.filter(name=settings.JOB_COACH).exists()

def info_man_user(user):
    return admin_user(user) or user.groups.filter(name=settings.JOB_COACH).exists()

def partner_user(user):
    return info_man_user(user) or user.groups.filter(name=settings.PARTNER).exists()

# as seen in tio approval for shirlie staff
def supply_chain_man_user(user):
    return admin_user(user) or user.groups.filter(name=settings.SUPPLY_CHAIN_MAN).exists()

def supply_chain_partner_user(user):
    return admin_user(user) or user.groups.filter(name=settings.SUPPLY_CHAIN_PART).exists()

def show_form_error(request, messages, msg, inform_support):
    messages.error(request, msg)

def set_deletion_status_in_js_data(js_dict, user, security_fn):
    js_dict['delete_allowed'] = security_fn(user)
