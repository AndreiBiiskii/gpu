from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.template.context_processors import request

from device.variables import *
from dateutil.relativedelta import relativedelta
from django import forms
from .models import *


class AddEquipmentForm(forms.Form):
    serial_number = forms.CharField(label='Серийный номер', max_length=100,
                                    widget=forms.TextInput(attrs={'class': 'type2'}))
    model = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}),
                                   queryset=EquipmentModel.objects.all(),
                                   label='Модель', required=False)
    model_new = forms.CharField(label='Добавить модель:', widget=forms.TextInput(attrs={'class': 'type2'}),
                                required=False)
    type = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}), label='Тип оборудования:',
                                  queryset=EquipmentType.objects.all(), required=False)
    type_new = forms.CharField(label='Добавить тип:', max_length=15, widget=forms.TextInput(attrs={'class': 'type2'}),
                               required=False)
    manufacturer = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}), label='Производитель:',
                                          queryset=Manufacturer.objects.all(), required=False)
    manufacturer_new = forms.CharField(label='Добавить производителя:',
                                       widget=forms.TextInput(attrs={'class': 'type2'}),
                                       required=False)
    name = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}), queryset=EquipmentName.objects.all(),
                                  required=False, label='Наименование:')
    name_new = forms.CharField(label='Добавить наименование:', widget=forms.TextInput(attrs={'class': 'type2'}),
                               required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'type2'}), label='Комментарий:')
    position = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}), queryset=GP.objects.all(),
                                      label='Поз. по ГП')
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'type2'}), max_length=50, required=False,
                               label='Место установки:')
    tag = forms.CharField(label='Тег', widget=forms.TextInput(attrs={'class': 'type2'}), max_length=100, required=False)
    status = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}), queryset=StatusAdd.objects.all(),
                                    label='Статус', required=False)
    status_new = forms.CharField(label='Добавить статус', max_length=10,
                                 widget=forms.TextInput(attrs={'class': 'type2'}), required=False)
    year = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}), label='Год выпуска:',
                                  queryset=Year.objects.all(), required=False)

    def clean(self):
        if Equipment.objects.filter(serial_number=self.cleaned_data['serial_number'],
                                    model=self.cleaned_data['model']):
            raise forms.ValidationError(message='Оборудование уже есть.')
        if (self.cleaned_data['model'] is None) & (self.cleaned_data['model_new'] == ''):
            raise forms.ValidationError(message='Не указана модель.')
        if len(self.cleaned_data['model_new']) > 100:
            raise forms.ValidationError(message='Модель должен быть до 100 символов.')
        if (self.cleaned_data['manufacturer'] is None) & (self.cleaned_data['manufacturer_new'] == ''):
            raise forms.ValidationError(message='Не указан производитель.')
        if len(self.cleaned_data['manufacturer_new']) > 100:
            raise forms.ValidationError(message='Производитель должен быть до 100 символов.')
        if (self.cleaned_data['name'] is None) & (self.cleaned_data['name_new'] == ''):
            raise forms.ValidationError(message='Не указано наименование.')
        if len(self.cleaned_data['name_new']) > 100:
            raise forms.ValidationError(message='Наименование должно быть до 100 символов')
        if self.cleaned_data['year'] is None:
            raise forms.ValidationError(message='Не указан год выпуска.')
        if self.cleaned_data['year'].name > datetime.datetime.now().year:
            raise forms.ValidationError(message='Год выпуска не может быть больше текущего')
        if (self.cleaned_data['status'] is None) & (self.cleaned_data['status_new'] == ''):
            raise forms.ValidationError(message='Не указан статус.')
        if (self.cleaned_data['type'] is None) & (self.cleaned_data['type_new'] == ''):
            raise forms.ValidationError(message='Не указан тип оборудования.')
        if self.cleaned_data['type_new']:
            self.cleaned_data['type'] = self.cleaned_data['type_new']
        if self.cleaned_data['manufacturer_new']:
            self.cleaned_data['manufacturer'] = self.cleaned_data['manufacturer_new']
        if self.cleaned_data['name_new']:
            self.cleaned_data['name'] = self.cleaned_data['name_new']
        if self.cleaned_data['model_new']:
            self.cleaned_data['model'] = self.cleaned_data['model_new']
        if self.cleaned_data['status_new']:
            self.cleaned_data['status'] = self.cleaned_data['status_new']

        if Equipment.objects.filter(
                Q(serial_number=self.cleaned_data['serial_number']) & Q(model__name=self.cleaned_data['model'])):
            raise forms.ValidationError(message='Оборудование уже есть.')
        return self.cleaned_data

    def save(self, user):
        description = self.cleaned_data.pop('description')
        if len(description) < 5:
            raise forms.ValidationError(message='Добавьте описание.')
        position = self.cleaned_data.pop('position')
        location = self.cleaned_data.pop('location')
        tag = self.cleaned_data.pop('tag')
        self.cleaned_data['si_or'] = False
        EquipmentType.objects.get_or_create(name=self.cleaned_data['type'])
        Manufacturer.objects.get_or_create(name=self.cleaned_data['manufacturer'])
        EquipmentName.objects.get_or_create(name=self.cleaned_data['name'])
        EquipmentModel.objects.get_or_create(name=self.cleaned_data['model'])
        StatusAdd.objects.get_or_create(name=self.cleaned_data['status'])
        equipment = Equipment.objects.create(serial_number=self.cleaned_data['serial_number'],
                                             type=EquipmentType.objects.get(name=self.cleaned_data['type']),
                                             manufacturer=Manufacturer.objects.get(
                                                 name=self.cleaned_data['manufacturer']),
                                             name=EquipmentName.objects.get(name=self.cleaned_data['name']),
                                             model=EquipmentModel.objects.get(name=self.cleaned_data['model']),
                                             year=Year.objects.get(name=self.cleaned_data['year'].name),
                                             si_or=False,
                                             )
        status = StatusAdd.objects.get(name=self.cleaned_data['status'])
        Status.objects.create(equipment=equipment, name=status)
        Tag.objects.create(equipment=equipment, name=tag)
        Location.objects.create(equipment=equipment, name=location)
        Position.objects.create(equipment=equipment, name=position)
        Description.objects.create(equipment=equipment, user=user, name=description)

        return self.cleaned_data


class AddDeviceForm(forms.Form):
    serial_number = forms.CharField(label='Серийный номер', max_length=100,
                                    widget=forms.TextInput(attrs={'class': 'type2'}))
    model = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}),
                                   queryset=EquipmentModel.objects.all(),
                                   label='Модель', required=False, )
    model_new = forms.CharField(label='Добавить модель:', widget=forms.TextInput(attrs={'class': 'type2'}),
                                required=False)
    type = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}), label='Тип оборудования:',
                                  queryset=EquipmentType.objects.all(), required=False)
    type_new = forms.CharField(label='Добавить тип:', max_length=15, widget=forms.TextInput(attrs={'class': 'type2'}),
                               required=False)
    manufacturer = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}), label='Производитель:',
                                          queryset=Manufacturer.objects.all(), required=False)
    manufacturer_new = forms.CharField(label='Добавить производителя:',
                                       widget=forms.TextInput(attrs={'class': 'type2'}),
                                       required=False)
    name = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}), queryset=EquipmentName.objects.all(),
                                  required=False, label='Наименование:')
    name_new = forms.CharField(label='Добавить наименование:', widget=forms.TextInput(attrs={'class': 'type2'}),
                               required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'type2'}), label='Комментарий:')
    position = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}), queryset=GP.objects.all(),
                                      label='Поз. по ГП')
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'type2'}), max_length=50, required=False,
                               label='Место установки:')
    tag = forms.CharField(label='Тег', widget=forms.TextInput(attrs={'class': 'type2'}), max_length=100)
    status = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}), queryset=StatusAdd.objects.all(),
                                    label='Статус', required=False)
    status_new = forms.CharField(label='Добавить статус', max_length=255,
                                 widget=forms.TextInput(attrs={'class': 'type2'}), required=False)
    year = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}), label='Год выпуска:',
                                  queryset=Year.objects.all(), required=False)
    reg_number = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}), label='Регистрационный номер:',
                                        queryset=RegNumber.objects.all(),
                                        required=False)
    reg_number_new = forms.CharField(widget=forms.TextInput(attrs={'class': 'type2'}),
                                     label='Добавить регистрационный номер:', max_length=20, required=False)
    previous_verification = forms.DateField(label='Дата предыдущей поверки:', widget=forms.TextInput(attrs=
    {
        'type': 'date',
        'class': 'type2',
    }))
    certificate = forms.CharField(widget=forms.TextInput(attrs={"class": "type2"}), label='Сертификат:')
    interval = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select'}), label='Межповерочный интервал:',
                                 choices=CHOICES_INTERVAL)
    min_scale = forms.DecimalField(widget=forms.TextInput(attrs={"class": "type2"}), label='Мин. шкалы:')
    max_scale = forms.DecimalField(widget=forms.TextInput(attrs={"class": "type2"}), label='Макс. шкалы:')
    unit = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}),
                             label='Единицы измерения:', queryset=Unit.objects.all(), required=False)
    unit_new = forms.CharField(widget=forms.TextInput(attrs={'class': 'type2'}))

    def clean(self):
        if Equipment.objects.filter(serial_number=self.cleaned_data['serial_number'],
                                    model=self.cleaned_data['model']):
            raise forms.ValidationError(message='Оборудование уже есть.')
        if (self.cleaned_data['model'] is None) & (self.cleaned_data['model_new'] == ''):
            raise forms.ValidationError(message='Не указана модель.')
        if self.cleaned_data['tag'] == '':
            self.cleaned_data['tag'] = ' '
        if len(self.cleaned_data['model_new']) > 100:
            raise forms.ValidationError(message='Модель должен быть до 100 символов.')
        if (self.cleaned_data['manufacturer'] is None) & (self.cleaned_data['manufacturer_new'] == ''):
            raise forms.ValidationError(message='Не указан производитель.')
        if len(self.cleaned_data['manufacturer_new']) > 100:
            raise forms.ValidationError(message='Производитель должен быть до 100 символов.')
        if (self.cleaned_data['name'] is None) & (self.cleaned_data['name_new'] == ''):
            raise forms.ValidationError(message='Не указано наименование.')
        if len(self.cleaned_data['name_new']) > 100:
            raise forms.ValidationError(message='Наименование должно быть до 100 символов')
        if self.cleaned_data['year'] is None:
            raise forms.ValidationError(message='Не указан год выпуска.')
        if self.cleaned_data['year'].name > datetime.datetime.now().year:
            raise forms.ValidationError(message='Год выпуска не может быть больше текущего')
        if (self.cleaned_data['status'] is None) & (self.cleaned_data['status_new'] == ''):
            raise forms.ValidationError(message='Не указан статус.')
        # if (self.cleaned_data['error'] is None) & (self.cleaned_data['error_new'] == ''):
        #     raise forms.ValidationError(message='Не указана погрешность.')
        if (self.cleaned_data['name'] is None) & (self.cleaned_data['name_new'] == ''):
            raise forms.ValidationError(message='Не указано наименование.')
        if (self.cleaned_data['type'] is None) & (self.cleaned_data['type_new'] == ''):
            raise forms.ValidationError(message='Не указан тип оборудования.')
        if (self.cleaned_data['reg_number'] is None) & (self.cleaned_data['reg_number_new'] == ''):
            raise forms.ValidationError(message='Не указан регистрационный номер.')
        if self.cleaned_data['type_new']:
            self.cleaned_data['type'] = self.cleaned_data['type_new']
        if self.cleaned_data['manufacturer_new']:
            self.cleaned_data['manufacturer'] = self.cleaned_data['manufacturer_new']
        if self.cleaned_data['name_new']:
            self.cleaned_data['name'] = self.cleaned_data['name_new']
        if self.cleaned_data['model_new']:
            self.cleaned_data['model'] = self.cleaned_data['model_new']
        if self.cleaned_data['status_new']:
            self.cleaned_data['status'] = self.cleaned_data['status_new']
        if self.cleaned_data['reg_number_new']:
            self.cleaned_data['reg_number'] = self.cleaned_data['reg_number_new']
        if self.cleaned_data['unit_new']:
            self.cleaned_data['unit'] = self.cleaned_data['unit_new']
        if Equipment.objects.filter(
                Q(serial_number=self.cleaned_data['serial_number']) & Q(model__name=self.cleaned_data['model'])):
            raise forms.ValidationError(message='Оборудование уже есть.')
        return self.cleaned_data

    def save(self, user):
        description = self.cleaned_data.pop('description')
        position = self.cleaned_data.pop('position')
        location = self.cleaned_data.pop('location')
        tag = self.cleaned_data.pop('tag')
        min_scale = self.cleaned_data.pop('min_scale')
        max_scale = self.cleaned_data.pop('max_scale')
        previous_verification = self.cleaned_data.pop('previous_verification')
        certificate = self.cleaned_data.pop('certificate')
        EquipmentType.objects.get_or_create(name=self.cleaned_data['type'])
        Manufacturer.objects.get_or_create(name=self.cleaned_data['manufacturer'])
        EquipmentName.objects.get_or_create(name=self.cleaned_data['name'])
        EquipmentModel.objects.get_or_create(name=self.cleaned_data['model'])
        StatusAdd.objects.get_or_create(name=self.cleaned_data['status'])
        equipment = Equipment.objects.create(serial_number=self.cleaned_data['serial_number'],
                                             type=EquipmentType.objects.get(name=self.cleaned_data['type']),
                                             manufacturer=Manufacturer.objects.get(
                                                 name=self.cleaned_data['manufacturer']),
                                             name=EquipmentName.objects.get(name=self.cleaned_data['name']),
                                             model=EquipmentModel.objects.get(name=self.cleaned_data['model']),
                                             year=Year.objects.get(name=self.cleaned_data['year'].name),

                                             )
        status = StatusAdd.objects.get(name=self.cleaned_data['status'])
        Status.objects.create(equipment=equipment, name=status)
        Tag.objects.create(equipment=equipment, name=tag)
        Location.objects.create(equipment=equipment, name=location)
        Position.objects.create(equipment=equipment, name=position)
        Description.objects.create(equipment=equipment, user=user, name=description)
        VerificationInterval.objects.get_or_create(name=self.cleaned_data['interval'])
        Scale.objects.get_or_create(min_scale=min_scale, max_scale=max_scale)
        # Error.objects.get_or_create(name=self.cleaned_data['error'])
        RegNumber.objects.get_or_create(name=self.cleaned_data['reg_number'])
        Unit.objects.get_or_create(name=self.cleaned_data['unit'])
        Si.objects.create(equipment=equipment,
                          previous_verification=previous_verification,
                          next_verification=previous_verification + relativedelta(
                              months=+(int(self.cleaned_data['interval']))),
                          certificate=certificate,
                          interval=VerificationInterval.objects.get(name=self.cleaned_data['interval']),
                          scale=Scale.objects.get(min_scale=min_scale, max_scale=max_scale),
                          unit=Unit.objects.get(name=self.cleaned_data['unit']),
                          # error_device=Error.objects.get(name=self.cleaned_data['error']),
                          reg_number=RegNumber.objects.get(name=self.cleaned_data['reg_number']))
        return self.cleaned_data


class SearchForm(forms.Form):
    serial_number = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))


class DraftForm(forms.ModelForm):
    poz_draft = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}), queryset=GP.objects.all(),
                                       label='Поз. по ГП')
    location_draft = forms.CharField(widget=forms.TextInput(attrs={'class': 'type2'}), label='Расположение')
    description_draft = forms.CharField(
        widget=forms.Textarea(attrs={"class": "type2"}), label='Комментарий:')
    tag_draft = forms.CharField(widget=forms.TextInput(attrs={'class': 'type2'}), label='Тэг:', required=False)
    status_draft = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}),
                                          queryset=StatusAdd.objects.all(),
                                          label='Статус')
    images = forms.ImageField(widget=forms.FileInput(attrs={'class': 'select'}))

    class Meta(object):
        model = Draft
        exclude = ('user_draft',)


class DraftFormDevice(forms.Form):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': '4', 'cols': '80'}))


class FormFilter(forms.Form):
    search = forms.ModelChoiceField(queryset=EquipmentType.objects.all())


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User name'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'User name'}))

    class Meta:
        model = User
        fields = ['username', 'password']

