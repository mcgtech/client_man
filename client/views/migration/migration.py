from client.models import Client
from common.models import Person, Note, Address, Telephone
from common.views import form_errors_as_array, super_user_or_job_coach, super_user_or_admin, show_form_error
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render
import json
import dateutil.parser

@login_required
@user_passes_test(super_user_or_admin, 'client_man_login')
def load_clients(request):
    json_data = open('static/json/clients.json')
    # deserialises it
    # need to eset created and last modified date
    json_clients = json.load(json_data)

    # TODO: get rid of imports that I dont need
    # TODO: chekc if client already exisits
    # TODO: trim strings
    # TODO: how to handle 'null'
    # TODO: I can pass the json obj directly into client contructor: http://stackoverflow.com/questions/21858465/json-file-reading-by-django
    # TODO: how will I handle addresses..
    # Create model instances for each item
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
                client.type = Person.CLIENT

                start_date = get_clean_json_data(json_client['start_date'])
                if len(start_date) > 0:
                    client.start_date = start_date
                end_date = get_clean_json_data(json_client['end_date'])
                if len(end_date) >0:
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

                client.save()

                # add address
                address = Address()
                address.line_1 = get_clean_json_data(json_client['line_1'])
                address.line_2 = get_clean_json_data(json_client['line_2'])
                address.line_3 = get_clean_json_data(json_client['line_3'])
                address.post_code = get_clean_json_data(json_client['post_code'])
                address.area = get_clean_json_data(json_client['area'])
                address.person = client
                address.save()

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

    return render(request, 'client/load_clients.html', {'json_clients': json_clients, 'items' : items, 'errors' :  errors})

def get_clean_json_data(json_data):
    if json_data is None:
        json_data = ''
    return json_data.strip()