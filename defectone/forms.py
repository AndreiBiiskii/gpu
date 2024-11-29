from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import ModelForm

from defectone.models import Approve, Defect, Contractor, Kait, Worker


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


class DefectAddForm(ModelForm):
    class Meta:
        model = Defect
        fields = (
            'defect', 'model', 'serial_number', 'defect_act', 'project', 'short_description', 'causes', 'gp',
            'location', 'tag', 'status', 'fix', 'operating_time', 'invest_letter', 'approve', 'contractor', 'kait',
            'worker',)
        widgets = {
            'defect': forms.HiddenInput(),
            'serial_number': forms.TextInput(attrs={'class': 'model'}),
            'defect_act': forms.TextInput(attrs={'class': 'model'}),
            'project': forms.TextInput(attrs={'class': 'model'}),
            'gp': forms.TextInput(attrs={'class': 'model'}),
            'location': forms.TextInput(attrs={'class': 'model'}),
            'tag': forms.TextInput(attrs={'class': 'model'}),
            'invest_letter': forms.TextInput(attrs={'class': 'model'}),
            'model': forms.TextInput(attrs={'class': 'model'}),
        }



        labels = {
            'defect': 'Оборудование',
            'model': 'Модель',
            'serial_number': 'Серийный номер',
            'defect_act': 'Номер дефектного акта'}
        # help_texts = {
        #     'defect': 'Укажите оборудование.',
        #     'model': 'Укажите модель.',
        #     'serial_number': 'Укажите серийный номер.',
        #     'defect_act': 'Укажите номер дефектного акта.'}
