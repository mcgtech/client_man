from client.models import Client
from django.db.models import Q
from common.views import job_coach_user, admin_user, job_coach_man_user

def find_client_by_full_name(query_name, user):
    qs = get_client_search_default_queryset(user)
    for term in query_name.split():
        qs = qs.filter(Q(forename__icontains=term) | Q(middle_name__icontains=term) | Q(surname__icontains=term))

    return qs


def get_client_search_default_queryset(user):
    qs = Client.objects.select_related('user').all()
    if job_coach_man_user(user) == False:
        qs = qs.filter(job_coach=user)

    return qs