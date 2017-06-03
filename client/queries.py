from client.models import Client
from django.db.models import Q
from common.views import job_coach_user, admin_user, job_coach_man_user, supply_chain_partner_user

def find_client_by_full_name(query_name, user):
    qs = get_client_search_default_queryset(user)
    for term in query_name.split():
        qs = qs.filter(Q(forename__icontains=term) | Q(middle_name__icontains=term) | Q(surname__icontains=term))

    return qs


def get_client_search_default_queryset(user):
    qs = Client.objects.select_related('user').all()
    if job_coach_man_user(user) == False:
        if job_coach_user(user):
            # qs = get_clients_where_user_is_current_coach(user, qs)
            qs = qs.filter(latest_contract__job_coach=user).distinct()
        elif supply_chain_partner_user(user):
            qs = qs.filter(latest_contract__partner=user).distinct()
        else:
            qs = Client.objects.none()
    return qs

# this is quite slow and would need speeding up if I use it
# see - I now store a link to latest contract in client
# but I have left this code here for illustration purposes
def get_clients_where_user_is_current_coach(user, qs):
    # only return clients where user is current job coach
    from client.models import Contract
    client_ids = []
    for client in qs:
        # default ordering now set in contract META section
        # latest_con = Contract.objects.filter(client=client).order_by('start_date').last()
        latest_con = Contract.objects.filter(client=client).last()
        if latest_con is not None and latest_con.job_coach == user:
            client_ids.append(latest_con.client.id)

    return qs.filter(pk__in=client_ids)