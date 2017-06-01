from .models import HTMLTemplate
from django_tables2 import tables, LinkColumn, A

class HTMLTempTable(tables.Table):
    # https://stackoverflow.com/questions/33184108/how-to-change-display-text-in-django-tables-2-link-column
    # http://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#linkcolumn
    id = LinkColumn('html_temp_edit', text=lambda record: record.id, args=[A('pk')], attrs={'a': {'target': '_blank'}})

    class Meta:
        model = HTMLTemplate
        # fiels to display in table
        fields = ('template_identifier', 'type')
        attrs = {"class": "paleblue table table-striped table-hover table-bordered"}
        sequence = ('id', '...')