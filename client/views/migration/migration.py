from client.models import Client, Contract, TIOContract, ContractStatus
from common.models import Person, Note, Address, Telephone
from common.views import form_errors_as_array, job_coach_user, job_coach_man_user, admin_user, show_form_error
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render
import json
import dateutil.parser
from django.conf import settings

@login_required
@user_passes_test(admin_user, 'client_man_login')
def load_contracts(request):
    # how I got the latest non tio rec in each group: https://www.xaprb.com/blog/2006/12/07/how-to-select-the-firstleastmax-row-per-group-in-sql/
    contract_json_data = open('static/json/contracts.json')
    tio_details_json_data = open('static/json/tio_details.json')
    # deserialises them
    json_contracts = json.load(contract_json_data)
    json_tio_details = json.load(tio_details_json_data)
    # and_steve - a-g
    items = []
    errors = []
    Contract.objects.all().delete()
    gen_contract = True

    if gen_contract:
        all_clients = Client.objects.select_related('user').all()
        for json_contract in json_contracts:
            # create model instances...
            contract = None
            try:
                nid = get_clean_json_data(json_contract['nid'])
                try:
                    client = all_clients.get(original_client_id=nid)
                    if client is not None:
                        con_type = int(get_clean_json_data(json_contract['con_type']))
                        if (con_type == Contract.TIO):
                            contract = TIOContract(client=client)
                        else:
                            contract = Contract(client=client)
                        contract.type = con_type
                        created_by, created_on, modified_by, modified_on = get_auditable_data(json_contract)

                        contract.created_by = created_by
                        contract.modified_by = modified_by
                        contract.created_on = created_on
                        contract.modified_on = modified_on

                        # I set USE_TZ = False in settings to get this to work
                        con_start_date = get_clean_json_data(json_contract['con_start_date'])
                        if len(con_start_date) > 0:
                            start_date = dateutil.parser.parse(con_start_date);
                            contract.start_date = start_date
                        con_end_date = get_clean_json_data(json_contract['con_end_date'])
                        if len(con_end_date) > 0:
                            end_date = dateutil.parser.parse(con_end_date);
                            contract.end_date = end_date
                        con_app_date = get_clean_json_data(json_contract['con_app_date'])
                        if len(con_app_date) > 0:
                            referral_date = dateutil.parser.parse(con_app_date);
                            contract.referral_date = referral_date
                        sec_client_group = get_clean_json_data(json_contract['sec_client_group'])
                        if len(sec_client_group) == 0 or sec_client_group == '-1' or sec_client_group== -1:
                            sec_client_group = None
                        contract.secondary_client_group = sec_client_group
                        if (con_type == Contract.TIO):
                            apply_tio_details(nid, contract, json_tio_details)
                        else:
                            contract.save()
                            add_contract_status(contract, created_by, created_on, modified_by,
                                                modified_on, get_clean_json_data(json_contract['con_state']))
                    else:
                        raise ValueError('Client not found for contract(1), client nid: ' + nid)
                except Exception as e:
                    raise ValueError('Client not found for contract(2), client nid: ' + nid + ', ' + str(e))

                    items.append(contract)
            except Exception as e:
                name = get_clean_json_data(json_contract['sec_client_group'])
                if contract != None:
                    es = str(contract) + ' ' + str(e)
                else:
                    es = 'Contract not created yet for ' + name + ', exception: ' + str(e)
                errors.append(es)

    return render(request, 'client/migration/migration.html', {'items' : items, 'form_errors' :  errors})


def get_auditable_data(json_data):
    created_by_user_name = get_clean_json_data(json_data['created_by'])
    created_by_list = User.objects.filter(username=created_by_user_name)
    created_by = created_by_list.first()
    modified_by_user_name = get_clean_json_data(json_data['modified_by'])
    modified_by_list = User.objects.filter(username=modified_by_user_name)
    modified_by = modified_by_list.first()
    # I set USE_TZ = False in settings to get this to work
    created_on = dateutil.parser.parse(get_clean_json_data(json_data['created_on']));
    modified_on = dateutil.parser.parse(get_clean_json_data(json_data['modified_on']));
    return created_by, created_on, modified_by, modified_on


def add_contract_status(contract, created_by, created_on, modified_by, modified_on, status):
    contract_status = ContractStatus()
    contract_status.contract = contract
    contract_status.created_by = created_by
    contract_status.modified_by = modified_by
    contract_status.created_on = created_on
    contract_status.modified_on = modified_on
    contract_status.status = status
    contract_status.save()


def apply_tio_details(nid, contract, json_tio_details):
    # try and find a tio version row created on same day as contract was saved in main details
    md_rec_last_changed = contract.created_on.strftime(settings.DISPLAY_DATE)
    md_rec_last_changed = dateutil.parser.parse(md_rec_last_changed) # get rid of time
    # print('Con created: ' + md_rec_last_changed + ' by ' + str(contract.created_by))
    tio_nid_match = None
    if nid in json_tio_details['data']:
        # iterate around each tio node they are in latest first order
        for tio_nid, tio_node in json_tio_details['data'][nid].items():
            tio_ver_mod_on = dateutil.parser.parse(get_clean_json_data(tio_node['modified_on']))
            tio_ver_mod_on = tio_ver_mod_on.strftime(settings.DISPLAY_DATE)
            tio_ver_mod_on = dateutil.parser.parse(tio_ver_mod_on) # get rid of time
            # print(md_rec_last_changed.strftime(settings.DISPLAY_DATE) + ' ' + tio_ver_mod_on.strftime(settings.DISPLAY_DATE) + ' ' + tio_nid)
            if md_rec_last_changed >= tio_ver_mod_on:
                # print(md_rec_last_changed.strftime(settings.DISPLAY_DATE) + ' ' + tio_ver_mod_on.strftime(settings.DISPLAY_DATE) + ' ' + tio_nid)
                tio_nid_match = tio_nid
                # print('tio_nid_match: ' + tio_nid_match)
                break
            # print(last_version['nid'] + ' ' + last_version['vid'] + ' ' + last_version['created_by'] + ' ' + tio_ver_created_on)
    try:
        if tio_nid_match is not None:
            tio_node = json_tio_details['data'][nid][tio_nid_match]
            if tio_node is not None:
                contract.aa_progress_jsa_18 = get_clean_json_data(tio_node['aa_progress_jsa_18'])
                contract.add_support_jsa_18 = get_clean_json_data(tio_node['add_support_jsa_18'])
                contract.add_support_jsa_25 = get_clean_json_data(tio_node['add_support_jsa_25'])
                contract.wca_incapacity = get_clean_json_data(tio_node['wca_incapacity'])
                contract.wrag_esa = get_clean_json_data(tio_node['wrag_esa'])
                contract.emp_pros_inc = get_clean_json_data(tio_node['emp_pros_inc'])
                contract.issue = get_clean_json_data(tio_node['issue'])
                contract.support_esa = get_clean_json_data(tio_node['support_esa'])
                contract.fund_mgr_notes = get_clean_json_data(tio_node['fund_mgr_notes'])
                contract.other_ben = get_clean_json_data(tio_node['other_ben'])
                contract.consent_form_complete = get_clean_json_data(tio_node['consent_form_complete'])
                closed_date = get_clean_json_data(tio_node['closed_date'])
                if len(closed_date) > 0:
                    closed_date = dateutil.parser.parse(closed_date);
                    contract.closed_date = closed_date
                partner_user_name = get_clean_json_data(tio_node['partner_id'])
                if len(partner_user_name) > 0:
                    partner_list = User.objects.filter(username=partner_user_name)
                    partner_user = partner_list.first()
                    contract.partner = partner_user
                contract.save()
                # add status for every tio version with a nid of tio_nid_match
                created_by, created_on, modified_by, modified_on = get_auditable_data(tio_node)
                add_contract_status(contract, created_by, created_on, modified_by, modified_on,
                                    get_clean_json_data(tio_node['con_state']))
        else:
             # save it even though there is no tio node created yet as it may not have be submitted yet
             contract.save()
    except Exception as e:
        print('nid: ' + nid + ' ' + str(e))

@login_required
@user_passes_test(admin_user, 'client_man_login')
def load_clients(request):
    # how I got the latest non tio rec in each group: https://www.xaprb.com/blog/2006/12/07/how-to-select-the-firstleastmax-row-per-group-in-sql/
    json_data = open('static/json/clients.json')
    # deserialises it
    # need to eset created and last modified date
    json_clients = json.load(json_data)
    # and_steve - a-g
    items = []
    errors = []

    Client.objects.all().delete()
    gen_client = True

    if gen_client:
        for json_client in json_clients:
            # create model instances...
            client = None
            try:
                #yourdate = dateutil.parser.parse(datestring)
                created_by_user_name = get_clean_json_data(json_client['created_by'])
                created_by_list = User.objects.filter(username=created_by_user_name)
                created_by = created_by_list.first()
                modified_by_user_name = get_clean_json_data(json_client['modified_by'])
                modified_by_list = User.objects.filter(username=modified_by_user_name)
                modified_by = modified_by_list.first()

                # I set USE_TZ = False in settings to get this to work
                created_on = dateutil.parser.parse(get_clean_json_data(json_client['created_on']));
                modified_on = dateutil.parser.parse(get_clean_json_data(json_client['modified_on']));
                home_phone = get_clean_json_data(json_client['home_phone'])
                mobile_phone = get_clean_json_data(json_client['mobile'])
                client = Client()

                start_date = get_clean_json_data(json_client['start_date'])
                if len(start_date) > 0:
                    client.start_date = start_date
                end_date = get_clean_json_data(json_client['end_date'])
                if len(end_date) > 0:
                    client.end_date = end_date
                client.title = get_clean_json_data(json_client['title'])
                client.middle_name = get_clean_json_data(json_client['middle_name'])
                client.known_as = get_clean_json_data(json_client['known_as'])
                client.dob = get_clean_json_data(json_client['dob'])
                client.forename = get_clean_json_data(json_client['forename'])
                client.surname = get_clean_json_data(json_client['surname'])
                client.email_address = get_clean_json_data(json_client['email_address'])
                client.sex = get_clean_json_data(json_client['sex'])
                client.known_as = get_clean_json_data(json_client['known_as'])
                client.marital_status = get_clean_json_data(json_client['marital_status'])
                client.ethnicity = get_clean_json_data(json_client['ethnicity'])
                client.nat_ins_number = get_clean_json_data(json_client['nat_ins_number'])
                client.recommended_by = get_clean_json_data(json_client['recommended_by'])
                client.social_work_involved = get_clean_json_data(json_client['social_work_involved'])
                client.ref_received = get_clean_json_data(json_client['ref_received'])
                jsa = get_clean_json_data(json_client['jsa'])
                if len(jsa) == 0:
                    jsa = Client.NO # default
                client.jsa = jsa
                education = get_clean_json_data(json_client['education'])
                if len(education) == 0:
                    education = Client.NO_QUAL # default
                client.education = education
                employment_status = get_clean_json_data(json_client['employment_status'])
                if len(employment_status) == 0 or employment_status == '-1' or employment_status == -1:
                    employment_status = None # default
                client.employment_status = employment_status
                stage = get_clean_json_data(json_client['stage'])
                if len(stage) == 0 or stage == '-1' or stage == -1:
                    stage = None # default
                client.stage = stage
                client_status = get_clean_json_data(json_client['client_status'])
                if len(client_status) == 0 or client_status == '-1' or client_status == -1:
                    client_status = None # default
                client.client_status = client_status
                time_unemployed = get_clean_json_data(json_client['time_unemployed'])
                if len(time_unemployed) == 0:
                    time_unemployed = Client.TBC # default
                client.time_unemployed = time_unemployed
                client_group = get_clean_json_data(json_client['client_group'])
                if len(client_group) == 0:
                    client_group = Client.TBA # default
                client.client_group = client_group
                client.created_by = created_by
                client.modified_by = modified_by
                client.created_on = created_on
                client.modified_on = modified_on

                 # associate with job coach - they need to be created before this runs
                job_coach_user_name = get_clean_json_data(json_client['job_coach'])
                job_coaches = User.objects.filter(username=job_coach_user_name)
                if len(job_coaches) > 0:
                    job_coach = job_coaches.first()
                    client.job_coach = job_coach
                else:
                    errors.append('Failed to find matching coach ' + job_coach_user_name + ' for ' + client.forename + ' ' + client.surname)
                client.original_client_id = get_clean_json_data(json_client['original_client_id'])


                # add address
                address = Address()
                address.line_1 = get_clean_json_data(json_client['line_1'])
                address.line_2 = get_clean_json_data(json_client['line_2'])
                address.line_3 = get_clean_json_data(json_client['line_3'])
                address.post_code = get_clean_json_data(json_client['post_code'])
                address.area = get_clean_json_data(json_client['area'])
                address.save()
                client.address = address
                client.save()

                # phones
                if len(home_phone) > 1:
                    home_tele = Telephone(type=Telephone.HOME, number=home_phone, person=client)
                    home_tele.save()
                if len(mobile_phone) > 1:
                    mobile_tele = Telephone(type=Telephone.MOBILE, number=mobile_phone, person=client)
                    mobile_tele.save()

                items.append(client)
            except Exception as e:
                if client != None:
                    es = client.forename + ' ' + client.surname + ' ' + str(e)
                else:
                    es = 'Client not created yet ' + str(e)
                errors.append(es)

    return render(request, 'client/migration/migration.html', {'json_clients': json_clients, 'items' : items, 'form_errors' :  errors})

def get_clean_json_data(json_data):
    if json_data is None:
        json_data = ''
    return json_data.strip()
