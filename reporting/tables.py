from .models import ReportTemplate
from django_tables2 import tables, LinkColumn, A

class ReportTempTable(tables.Table):
    # https://stackoverflow.com/questions/33184108/how-to-change-display-text-in-django-tables-2-link-column
    # http://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#linkcolumn
    id = LinkColumn('report_temp_edit', text=lambda record: record.id, args=[A('pk')], attrs={'a': {'target': '_blank'}})

    class Meta:
        model = ReportTemplate
        # fields to display in table
        fields = ('id', 'template_identifier', 'modified_by', 'modified_on')
        attrs = {"class": "paleblue table table-striped table-hover table-bordered"}
        sequence = ('id', 'template_identifier', 'modified_by', 'modified_on')