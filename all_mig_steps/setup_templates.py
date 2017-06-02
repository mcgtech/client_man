
from django.contrib.auth.models import User
from email_template.models import EmailTemplate
from reporting.models import ReportTemplate
from datetime import datetime

# setup email templates
admin = User.objects.get(pk=1)
accept_partner_temp = EmailTemplate(template_identifier=EmailTemplate.CON_ACCEPT)
accept_partner_temp.subject = '{{ agency_name }} - contract acceptance for client {{ client.id}}'
accept_partner_temp.from_address = '{{ gen_con_from_address }}'
accept_partner_temp.to_addresses = '{{ contract.partner.email }}'
accept_partner_temp.html_body = '<p>The latest contract for {{client.get_absolute_url_markup}} has just been accepted</p>'
accept_partner_temp.plain_body = 'The latest contract for {{client.get_absolute_url_markup}} has just been accepted'
accept_partner_temp.created_by = admin
accept_partner_temp.modified_by = admin
accept_partner_temp.created_on = datetime.now()
accept_partner_temp.modified_on = datetime.now()
accept_partner_temp.save()

approve_temp = EmailTemplate(template_identifier=EmailTemplate.CON_APPROVE)
approve_temp.subject = '{{ agency_name }} - contract approval for client {{ client.id}}'
approve_temp.gen_con_from_address = '{{ gen_con_from_address }}'
approve_temp.to_addresses = '{{ contract.created_by.email }}'
approve_temp.html_body = '<p>The latest contract for {{client.get_absolute_url_markup}} has just been approved</p>'
approve_temp.plain_body = 'The latest contract for {{client.get_absolute_url_markup}} has just been approved'
approve_temp.created_by = admin
approve_temp.modified_by = admin
approve_temp.created_on = datetime.now()
approve_temp.modified_on = datetime.now()
approve_temp.save()

revoke_temp = EmailTemplate(template_identifier=EmailTemplate.CON_REVOKE)
revoke_temp.subject = '{{ agency_name }} - contract revoked for client {{ client.id}}'
revoke_temp.from_address = '{{ gen_con_from_address }}'
revoke_temp.to_addresses = '{{ contract.partner.email }}'
revoke_temp.html_body = '<p>The latest contract for {{client.get_absolute_url_markup}} has just been revoked</p>'
revoke_temp.plain_body = 'The latest contract for {{client.get_absolute_url_markup}} has just been revoked'
revoke_temp.created_by = admin
revoke_temp.modified_by = admin
revoke_temp.created_on = datetime.now()
revoke_temp.modified_on = datetime.now()
revoke_temp.save()

reject_temp = EmailTemplate(template_identifier=EmailTemplate.CON_REJECT)
reject_temp.subject = '{{ agency_name }} - contract rejection for client {{ client.id}}'
reject_temp.from_address = '{{ gen_con_from_address }}'
reject_temp.to_addresses = '{{ contract.created_by.email }}'
reject_temp.html_body = '<p>The latest contract for {{client.get_absolute_url_markup}} has just been rejected</p>'
reject_temp.plain_body = 'The latest contract for {{client.get_absolute_url_markup}} has just been rejected'
reject_temp.created_by = admin
reject_temp.modified_by = admin
reject_temp.created_on = datetime.now()
reject_temp.modified_on = datetime.now()
reject_temp.save()

undo_temp = EmailTemplate(template_identifier=EmailTemplate.CON_UNDO)
undo_temp.subject = '{{ agency_name }} - contract approval undone for client {{ client.id}}'
undo_temp.from_address = '{{ gen_con_from_address }}'
undo_temp.to_addresses = '{{ contract.created_by.email }}'
undo_temp.html_body = '<p>The latest contract for {{client.get_absolute_url_markup}} has just had its approval undone</p>'
undo_temp.plain_body = 'The latest contract for {{client.get_absolute_url_markup}} has just had its approval undone'
undo_temp.created_by = admin
undo_temp.modified_by = admin
undo_temp.created_on = datetime.now()
undo_temp.modified_on = datetime.now()
undo_temp.save()

# setup reporting templates
client_dets_temp = ReportTemplate(template_identifier=ReportTemplate.CLIENT_MAIN)
client_dets_temp.created_by = admin
client_dets_temp.modified_by = admin
client_dets_temp.created_on = datetime.now()
client_dets_temp.modified_on = datetime.now()

client_con_temp = ReportTemplate(template_identifier=ReportTemplate.CLIENT_LATE_CON)
client_con_temp.created_by = admin
client_con_temp.modified_by = admin
client_con_temp.created_on = datetime.now()
client_con_temp.modified_on = datetime.now()
client_con_temp.save()

client_tio_con_temp = ReportTemplate(template_identifier=ReportTemplate.CLIENT_LATE_TIO_CON)
client_tio_con_temp.created_by = admin
client_tio_con_temp.modified_by = admin
client_tio_con_temp.created_on = datetime.now()
client_tio_con_temp.modified_on = datetime.now()

root = '/Users/stephenmcgonigal/django_projs'
with open(root + '/all_mig_steps/templates/client_dets_temp.html', 'r') as client_dets_file:
    client_dets_temp_html = client_dets_file.read()
with open(root + '/all_mig_steps/templates/client_con_temp.html', 'r') as client_con_file:
    client_con_html = client_con_file.read()
with open(root + '/all_mig_steps/templates/client_tio_con_temp.html', 'r') as client_tio_con_file:
    client_tio_con_html = client_tio_con_file.read()
client_dets_temp.body = client_dets_temp_html
client_con_temp.body = client_con_html
client_tio_con_temp.body = client_tio_con_html

client_dets_temp.save()
client_con_temp.save()
client_tio_con_temp.save()