from django.contrib.auth.models import User
from django.forms import ModelForm

from defectone.models import Approve


class PersonForm(ModelForm):
    class Meta:
        model = Approve
        fields = ['name', 'job_title', 'organization']


class AddUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', ]

    def save(self, user):
        user.email = self.cleaned_data['email']
        user.save()
