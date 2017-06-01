
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from email_template.models import EmailTemplate
from datetime import datetime
User.objects.create_superuser('admin', 'a@a.com', 'new3lifeok')
admin_group = Group(name="admin")
admin_group.save()
client_group = Group(name="client")
client_group.save()
neil = User.objects.create_user(username='neil', email="n.macleod@shirlie.co.uk",  password="neil_1234")
admin_group.user_set.add(neil)
admin_group.save()
job_coach_group = Group(name="job coach")
job_coach_group.save()
job_coach_mgr_group = Group(name="job coach manager")
job_coach_mgr_group.save()
partner_group = Group(name="partner")
partner_group.save()
info_man_group = Group(name="info manager")
info_man_group.save()
supply_chain_man_group = Group(name="supply chain manager")
supply_chain_man_group.save()
rag_tag_group = Group(name="rag tag")
rag_tag_group.save()
hicouncil_group = Group(name="highland council")
hicouncil_group.save()

# run sql to repopulate
ann = User.objects.create_user('ann', 'ann@ann.com', 'ann123');ann.is_staff=True;ann.save()
lindasutherland = User.objects.create_user('lindasutherland', 'lindasutherland@shirlie.co.uk', 'lindasutherland123');lindasutherland.is_staff=True;lindasutherland.save()
jobcoach = User.objects.create_user('jobcoach', 'jobcoach@gmail.com', 'jobcoach123');jobcoach.is_staff=True;jobcoach.save()
traceythomson = User.objects.create_user('traceythomson', 'traceythomson@shirlie.co.uk', 'traceythomson123');traceythomson.is_staff=True;traceythomson.save()
mattest = User.objects.create_user('mattest', 'mattest@a.com', 'mattest123');mattest.is_staff=True;mattest.save()
alanryndycz = User.objects.create_user('alanryndycz', 'alanryndycz@shirlie.co.uk', 'alanryndycz123');alanryndycz.is_staff=True;alanryndycz.save()
donnielamont = User.objects.create_user('donnielamont', 'donnielamont@shirlie.co.uk', 'donnielamont123');donnielamont.is_staff=True;donnielamont.save()
ellenreid = User.objects.create_user('ellenreid', 'ellenreid@shirlie.co.uk', 'ellenreid123');ellenreid.is_staff=True;ellenreid.save()
emmamackinnon = User.objects.create_user('emmamackinnon', 'emmamacKinnon@shirlie.co.uk', 'emmamackinnon123');emmamackinnon.is_staff=True;emmamackinnon.save()
harrygillespie = User.objects.create_user('harrygillespie', 'harrygillespie@shirlie.co.uk', 'harrygillespie123');harrygillespie.is_staff=True;harrygillespie.save()
jrynabatters = User.objects.create_user('jrynabatters', 'jrynabatters@shirlie.co.uk', 'jrynabatters123');jrynabatters.is_staff=True;jrynabatters.save()
laurenblack = User.objects.create_user('laurenblack', 'laurenblack@shirlie.co.uk', 'laurenblack123');laurenblack.is_staff=True;laurenblack.save()
lynneread = User.objects.create_user('lynneread', 'lynneread@shirlie.co.uk', 'lynneread123');lynneread.is_staff=True;lynneread.save()
marionscott = User.objects.create_user('marionscott', 'marionscott@shirlie.co.uk', 'marionscott123');marionscott.is_staff=True;marionscott.save()
marksmyth = User.objects.create_user('marksmyth', 'marksmyth@shirlie.co.uk', 'marksmyth123');marksmyth.is_staff=True;marksmyth.save()
moragabernethy = User.objects.create_user('moragabernethy', 'moragabernethy@shirlie.co.uk', 'moragabernethy123');moragabernethy.is_staff=True;moragabernethy.save()
neillianrodger = User.objects.create_user('neillianrodger', 'neillianrodger@shirlie.co.uk', 'neillianrodger123');neillianrodger.is_staff=True;neillianrodger.save()
robford = User.objects.create_user('robford', 'robford@shirlie.co.uk', 'robford123');robford.is_staff=True;robford.save()
sharoncameron = User.objects.create_user('sharoncameron', 'sharoncameron@shirlie.co.uk', 'sharoncameron123');sharoncameron.is_staff=True;sharoncameron.save()
shonaellis = User.objects.create_user('shonaellis', 'shonaellis@shirlie.co.uk', 'shonaellis123');shonaellis.is_staff=True;shonaellis.save()
simonetot = User.objects.create_user('simonetot', 'simoneduncan@shirlie.co.uk', 'simonetot123');simonetot.is_staff=True;simonetot.save()
annlee = User.objects.create_user('annlee', 'annlee@shirlie.co.uk', 'annlee123');annlee.is_staff=True;annlee.save()
maryfleming = User.objects.create_user('maryfleming', 'maryfleming@shirlie.co.uk', 'maryfleming123');maryfleming.is_staff=True;maryfleming.save()
christinebruce = User.objects.create_user('christinebruce', 'christinebruce@shirlie.co.uk', 'christinebruce123');christinebruce.is_staff=True;christinebruce.save()
lizgibson = User.objects.create_user('lizgibson', 'reception2@shirlie.co.uk', 'lizgibson123');lizgibson.is_staff=True;lizgibson.save()
reception = User.objects.create_user('reception', 'reception@shirlie.co.uk', 'reception123');reception.is_staff=True;reception.save()
stephwood = User.objects.create_user('stephwood', 'stephaniewood@shirlie.co.uk', 'stephwood123');stephwood.is_staff=True;stephwood.save()
infoman = User.objects.create_user('infoman', 'stevemcgonigal@yahoo.co.uk', 'infoman123');infoman.is_staff=True;infoman.save()
janemacdonald = User.objects.create_user('janemacdonald', 'janemacDonald@shirlie.co.uk', 'janemacdonald123');janemacdonald.is_staff=True;janemacdonald.save()
stephengibson = User.objects.create_user('stephengibson', 'stephengibson@shirlie.co.uk', 'stephengibson123');stephengibson.is_staff=True;stephengibson.save()
svqassessor = User.objects.create_user('svqassessor', 'svqassessor@svq.com', 'svqassessor123');svqassessor.is_staff=True;svqassessor.save()
jobcoach2 = User.objects.create_user('jobcoach2', 'mcgonigalstephen@gmail.com', 'jobcoach2123');jobcoach2.is_staff=True;jobcoach2.save()
fionahawthorne = User.objects.create_user('fionahawthorne', 'fionahawthorne@shirlie.co.uk', 'fionahawthorne123');fionahawthorne.is_staff=True;fionahawthorne.save()
angusmaclennan = User.objects.create_user('angusmaclennan', 'angusmaclennan@shirlie.co.uk', 'angusmaclennan123');angusmaclennan.is_staff=True;angusmaclennan.save()
minettemaclennan = User.objects.create_user('minettemaclennan', 'minettemaclennan@shirlie.co.uk', 'minettemaclennan123');minettemaclennan.is_staff=True;minettemaclennan.save()
jamesmacdonald = User.objects.create_user('jamesmacdonald', 'jamesmacdonald@shirlie.co.uk', 'jamesmacdonald123');jamesmacdonald.is_staff=True;jamesmacdonald.save()
markmackenzie = User.objects.create_user('markmackenzie', 'markmackenzie@shirlie.co.uk', 'markmackenzie123');markmackenzie.is_staff=True;markmackenzie.save()
lucybeattie = User.objects.create_user('lucybeattie', 'lucybeattie@shirlie.co.uk', 'lucybeattie123');lucybeattie.is_staff=True;lucybeattie.save()
paulsloan = User.objects.create_user('paulsloan', 'paulsloan@shirlie.co.uk', 'paulsloan123');paulsloan.is_staff=True;paulsloan.save()
jemmatweedie = User.objects.create_user('jemmatweedie', 'jemmatweedie@shirlie.co.uk', 'jemmatweedie123');jemmatweedie.is_staff=True;jemmatweedie.save()
ashleymurray = User.objects.create_user('ashleymurray', 'ashleymurray@shirlie.co.uk', 'ashleymurray123');ashleymurray.is_staff=True;ashleymurray.save()
kirsty = User.objects.create_user('kirsty', 'kirstygillies@shirlie.co.uk', 'kirsty123');kirsty.is_staff=True;kirsty.save()
hayleysangster = User.objects.create_user('hayleysangster', 'hayleysangster@shirlie.co.uk', 'hayleysangster123');hayleysangster.is_staff=True;hayleysangster.save()
judy = User.objects.create_user('judy', 'judyspark@shirlie.co.uk', 'judy123');judy.is_staff=True;judy.save()
meghanmackenzie = User.objects.create_user('meghanmackenzie', 'meghanmackenzie@shirlie.co.uk', 'meghanmackenzie123');meghanmackenzie.is_staff=True;meghanmackenzie.save()
jillian = User.objects.create_user('jillian', 'jillianbaird@shirlie.co.uk', 'jillian123');jillian.is_staff=True;jillian.save()
markdowney = User.objects.create_user('markdowney', 'm.downey@shirliie.co.uk', 'markdowney123');markdowney.is_staff=True;markdowney.save()
darrenhamilton = User.objects.create_user('darrenhamilton', 'd.hamilton@shirlie.co.uk', 'darrenhamilton123');darrenhamilton.is_staff=True;darrenhamilton.save()
heatherharper = User.objects.create_user('heatherharper', 'h.harper@shirlie.co.uk', 'heatherharper123');heatherharper.is_staff=True;heatherharper.save()
scottfraser = User.objects.create_user('scottfraser', 's.fraser@shirlie.co.uk', 'scottfraser123');scottfraser.is_staff=True;scottfraser.save()
dawncattanach = User.objects.create_user('dawncattanach', 'd.cattanach@shirlie.co.uk', 'dawncattanach123');dawncattanach.is_staff=True;dawncattanach.save()
closed = User.objects.create_user('closed', 'closed@closed', 'closed123');
neilmacleod = User.objects.create_user('neilmacleod', 'neilmacLeod@shirlie.co.uk', 'neilmacleod123');neilmacleod.save()
hicouncil = User.objects.create_user('hicouncil', 'highlandcouncil123@gmail.com', 'hicouncil123');hicouncil.save()
ragtag = User.objects.create_user('ragtag', 'ragtag1456@gmail.com', 'ragtag123');ragtag.save()
janegair = User.objects.create_user('janegair', 'Jane.gair@highland-opportunity.com', 'janegair123');janegair.save()
vickysamuels = User.objects.create_user('vickysamuels', 'vickisamuels@yahoo.co.uk', 'vickysamuels123');vickysamuels.save()
joan = User.objects.create_user('joan', 'joan.mackay@ragtagskye.org', 'joan123');joan.save()
hicounciluser = User.objects.create_user('hicounciluser', 'hicouncil@hicouncil.com', 'hicounciluser123');hicounciluser.save()
# run sql to repopulate
job_coach_group.user_set.add(ann)
job_coach_group.user_set.add(lindasutherland)
job_coach_group.user_set.add(jobcoach)
job_coach_group.user_set.add(traceythomson)
job_coach_group.user_set.add(mattest)
job_coach_group.user_set.add(alanryndycz)
job_coach_group.user_set.add(donnielamont)
job_coach_group.user_set.add(ellenreid)
job_coach_group.user_set.add(emmamackinnon)
job_coach_group.user_set.add(harrygillespie)
job_coach_group.user_set.add(jrynabatters)
job_coach_group.user_set.add(laurenblack)
job_coach_group.user_set.add(lynneread)
job_coach_group.user_set.add(marionscott)
job_coach_group.user_set.add(marksmyth)
job_coach_group.user_set.add(moragabernethy)
job_coach_group.user_set.add(neillianrodger)
job_coach_group.user_set.add(robford)
job_coach_group.user_set.add(sharoncameron)
job_coach_group.user_set.add(shonaellis)
job_coach_group.user_set.add(simonetot)
job_coach_group.user_set.add(annlee)
job_coach_group.user_set.add(maryfleming)
job_coach_group.user_set.add(christinebruce)
job_coach_group.user_set.add(lizgibson)
job_coach_group.user_set.add(reception)
job_coach_group.user_set.add(stephwood)
job_coach_group.user_set.add(infoman)
job_coach_group.user_set.add(janemacdonald)
job_coach_group.user_set.add(stephengibson)
job_coach_group.user_set.add(svqassessor)
job_coach_group.user_set.add(jobcoach2)
job_coach_group.user_set.add(fionahawthorne)
job_coach_group.user_set.add(angusmaclennan)
job_coach_group.user_set.add(minettemaclennan)
job_coach_group.user_set.add(jamesmacdonald)
job_coach_group.user_set.add(markmackenzie)
job_coach_group.user_set.add(lucybeattie)
job_coach_group.user_set.add(paulsloan)
job_coach_group.user_set.add(jemmatweedie)
job_coach_group.user_set.add(ashleymurray)
job_coach_group.user_set.add(kirsty)
job_coach_group.user_set.add(hayleysangster)
job_coach_group.user_set.add(judy)
job_coach_group.user_set.add(meghanmackenzie)
job_coach_group.user_set.add(jillian)
job_coach_group.user_set.add(markdowney)
job_coach_group.user_set.add(darrenhamilton)
job_coach_group.user_set.add(heatherharper)
job_coach_group.user_set.add(scottfraser)
job_coach_group.user_set.add(dawncattanach)
job_coach_group.user_set.add(closed)
partner_group.user_set.add(stephengibson)
partner_group.user_set.add(stephwood)
partner_group.user_set.add(ragtag)
partner_group.user_set.add(infoman)
partner_group.user_set.add(christinebruce)
partner_group.user_set.add(joan)
partner_group.user_set.add(vickysamuels)
partner_group.user_set.add(annlee)
partner_group.user_set.add(traceythomson)
job_coach_mgr_group.user_set.add(mattest)
job_coach_mgr_group.user_set.add(reception)
job_coach_mgr_group.user_set.add(jobcoach)
job_coach_mgr_group.user_set.add(stephwood)
job_coach_mgr_group.user_set.add(christinebruce)
job_coach_mgr_group.user_set.add(traceythomson)
job_coach_mgr_group.user_set.add(fionahawthorne)
job_coach_mgr_group.user_set.add(annlee)
job_coach_mgr_group.user_set.add(meghanmackenzie)
job_coach_mgr_group.user_set.add(jillian)
info_man_group.user_set.add(ann)
info_man_group.user_set.add(traceythomson)
info_man_group.user_set.add(lizgibson)
info_man_group.user_set.add(infoman)
info_man_group.user_set.add(stephwood)
info_man_group.user_set.add(christinebruce)
info_man_group.user_set.add(maryfleming)
info_man_group.user_set.add(fionahawthorne)
info_man_group.user_set.add(stephengibson)
info_man_group.user_set.add(annlee)
info_man_group.user_set.add(meghanmackenzie)
info_man_group.user_set.add(jillian)
supply_chain_man_group.user_set.add(stephengibson)
supply_chain_man_group.user_set.add(stephwood)
supply_chain_man_group.user_set.add(infoman)
supply_chain_man_group.user_set.add(christinebruce)
supply_chain_man_group.user_set.add(traceythomson)
supply_chain_man_group.user_set.add(annlee)
hicouncil_group.user_set.add(hicouncil)
hicouncil_group.user_set.add(janegair)
hicouncil_group.user_set.add(hicounciluser)
hicouncil_group.user_set.add(neilmacleod)
rag_tag_group.user_set.add(ragtag)
rag_tag_group.user_set.add(joan)
rag_tag_group.user_set.add(vickysamuels)

job_coach_group.save()
partner_group.save()
job_coach_mgr_group.save()
info_man_group.save()
supply_chain_man_group.save()
hicouncil_group.save()
rag_tag_group.save()

# setup email templates
admin = User.objects.get(pk=1)
accept_partner_temp = EmailTemplate(template_identifier=EmailTemplate.CON_ACCEPT)
accept_partner_temp.subject = '{{ agency_name }} - contract acceptance for {{ client.get_full_name}}'
accept_partner_temp.from_address = '{{ gen_con_from_address }}'
accept_partner_temp.to_addresses = '{{ contract.partner.email }}'
accept_partner_temp.html_body = '<p>The latest contract for {{client.get_full_name}} has just been accepted</p>'
accept_partner_temp.plain_body = 'The latest contract for {{client.get_full_name}} has just been accepted'
accept_partner_temp.created_by = admin
accept_partner_temp.modified_by = admin
accept_partner_temp.created_on = datetime.now()
accept_partner_temp.modified_on = datetime.now()
accept_partner_temp.save()

approve_temp = EmailTemplate(template_identifier=EmailTemplate.CON_APPROVE)
approve_temp.subject = '{{ agency_name }} - contract approval for {{ client.get_full_name}}'
approve_temp.gen_con_from_address = '{{ gen_con_from_address }}'
approve_temp.to_addresses = '{{ contract.created_by.email }}'
approve_temp.html_body = '<p>The latest contract for {{client.get_full_name}} has just been approved</p>'
approve_temp.plain_body = 'The latest contract for {{client.get_full_name}} has just been approved'
approve_temp.created_by = admin
approve_temp.modified_by = admin
approve_temp.created_on = datetime.now()
approve_temp.modified_on = datetime.now()
approve_temp.save()

revoke_temp = EmailTemplate(template_identifier=EmailTemplate.CON_REVOKE)
revoke_temp.subject = '{{ agency_name }} - contract revoked for {{ client.get_full_name}}'
revoke_temp.from_address = '{{ gen_con_from_address }}'
revoke_temp.to_addresses = '{{ contract.partner.email }}'
revoke_temp.html_body = '<p>The latest contract for {{client.get_full_name}} has just been revoked</p>'
revoke_temp.plain_body = 'The latest contract for {{client.get_full_name}} has just been revoked'
revoke_temp.created_by = admin
revoke_temp.modified_by = admin
revoke_temp.created_on = datetime.now()
revoke_temp.modified_on = datetime.now()
revoke_temp.save()

reject_temp = EmailTemplate(template_identifier=EmailTemplate.CON_REJECT)
reject_temp.subject = '{{ agency_name }} - contract rejection for {{ client.get_full_name}}'
reject_temp.from_address = '{{ gen_con_from_address }}'
reject_temp.to_addresses = '{{ contract.created_by.email }}'
reject_temp.html_body = '<p>The latest contract for {{client.get_full_name}} has just been rejected</p>'
reject_temp.plain_body = 'The latest contract for {{client.get_full_name}} has just been rejected'
reject_temp.created_by = admin
reject_temp.modified_by = admin
reject_temp.created_on = datetime.now()
reject_temp.modified_on = datetime.now()
reject_temp.save()