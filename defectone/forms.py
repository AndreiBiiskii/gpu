from django.forms import ModelForm

from defectone.models import Approve


class PersonForm(ModelForm):
    class Meta:
        model = Approve
        fields = ['name', 'job_title', 'organization']

