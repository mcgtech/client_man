
from django.contrib.auth.models import User
from email_template.models import EmailTemplate
from reporting.models import ReportTemplate
from datetime import datetime

with open('/Users/stephenmcgonigal/django_projs/all_mig_steps/templates/client_dets_temp.html', 'r') as client_dets_file:
    client_dets_temp_html = client_dets_file.read()
    print(client_dets_temp_html)
