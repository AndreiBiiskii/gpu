from IPython.utils.coloransi import value
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.forms import ModelForm
from urllib3 import request

from device.variables import *
from dateutil.relativedelta import relativedelta
from django import forms
from .models import *


class AddEquipmentForm(forms.Form):
    serial_number = forms.CharField(label='Серийный номер', max_length=255,
                                    widget=forms.TextInput(attrs={'class': 'type2'}))
    model = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}),
                                   queryset=EquipmentModel.objects.all(),
                                   label='Модель', required=False)
    model_new = forms.CharField(label='Добавить модель:', widget=forms.TextInput(attrs={'class': 'type2'}),
                                required=False)
    # type = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}), label='Тип оборудования:',
    #                               queryset=EquipmentType.objects.all(), required=False)
    # type_new = forms.CharField(label='Добавить тип:', max_length=255, widget=forms.TextInput(attrs={'class': 'type2'}),
    #                            required=False)
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
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'type2'}), required=False, label='Примечание:')
    position = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}), queryset=GP.objects.all(),
                                      label='Поз. по ГП', required=False)
    position_new = forms.CharField(widget=forms.TextInput(attrs={'class': 'type2'}),
                                   label='Добавить позицию по ГП:', max_length=20, required=False)
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'type2'}), max_length=255, required=False,
                               label='Место установки:')
    tag = forms.CharField(label='Тег', widget=forms.TextInput(attrs={'class': 'type2'}), max_length=255, required=False)
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
        if len(self.cleaned_data['model_new']) > 255:
            raise forms.ValidationError(message='Модель должен быть до 255 символов.')
        if (self.cleaned_data['manufacturer'] is None) & (self.cleaned_data['manufacturer_new'] == ''):
            raise forms.ValidationError(message='Не указан производитель.')
        if len(self.cleaned_data['manufacturer_new']) > 255:
            raise forms.ValidationError(message='Производитель должен быть до 255 символов.')
        if (self.cleaned_data['name'] is None) & (self.cleaned_data['name_new'] == ''):
            raise forms.ValidationError(message='Не указано наименование.')
        if len(self.cleaned_data['name_new']) > 255:
            raise forms.ValidationError(message='Наименование должно быть до 255 символов')
        if self.cleaned_data['year'] is None:
            raise forms.ValidationError(message='Не указан год выпуска.')
        if self.cleaned_data['year'].name > datetime.datetime.now().year:
            raise forms.ValidationError(message='Год выпуска не может быть больше текущего')
        if (self.cleaned_data['status'] is None) & (self.cleaned_data['status_new'] == ''):
            raise forms.ValidationError(message='Не указан статус.')
        # if (self.cleaned_data['type'] is None) & (self.cleaned_data['type_new'] == ''):
        #     raise forms.ValidationError(message='Не указан тип оборудования.')
        # if len(self.cleaned_data['description']) < 5:
        #     raise forms.ValidationError(message='Добавьте описание.')
        # if self.cleaned_data['type_new']:
        #     self.cleaned_data['type'] = self.cleaned_data['type_new']
        if self.cleaned_data['manufacturer_new']:
            self.cleaned_data['manufacturer'] = self.cleaned_data['manufacturer_new']
        if self.cleaned_data['name_new']:
            self.cleaned_data['name'] = self.cleaned_data['name_new']
        if self.cleaned_data['model_new']:
            self.cleaned_data['model'] = self.cleaned_data['model_new']
        if self.cleaned_data['status_new']:
            self.cleaned_data['status'] = self.cleaned_data['status_new']
        if self.cleaned_data['position_new']:
            self.cleaned_data['position'] = self.cleaned_data['position_new']
        if (self.cleaned_data['position_new'] == '') and (self.cleaned_data['position'] is None):
            raise forms.ValidationError(message='Не указана позиция по ГП')
        if Equipment.objects.filter(
                Q(serial_number=self.cleaned_data['serial_number']) & Q(model__name=self.cleaned_data['model'])):
            raise forms.ValidationError(message='Оборудование уже есть.')
        return self.cleaned_data

    def save(self, user):
        description = self.cleaned_data.pop('description')
        position = self.cleaned_data.pop('position')
        location = self.cleaned_data.pop('location')
        tag = self.cleaned_data.pop('tag')
        self.cleaned_data['si_or'] = False
        # EquipmentType.objects.get_or_create(name=self.cleaned_data['type'])
        Manufacturer.objects.get_or_create(name=self.cleaned_data['manufacturer'])
        EquipmentName.objects.get_or_create(name=self.cleaned_data['name'])
        EquipmentModel.objects.get_or_create(name=self.cleaned_data['model'])
        StatusAdd.objects.get_or_create(name=self.cleaned_data['status'])
        equipment = Equipment.objects.create(serial_number=self.cleaned_data['serial_number'],
                                             # type=EquipmentType.objects.get(name=self.cleaned_data['type']),
                                             manufacturer=Manufacturer.objects.get(
                                                 name=self.cleaned_data['manufacturer']),
                                             name=EquipmentName.objects.get(name=self.cleaned_data['name']),
                                             model=EquipmentModel.objects.get(name=self.cleaned_data['model']),
                                             year=Year.objects.get(name=self.cleaned_data['year'].name),
                                             si_or=False,
                                             comment=self.cleaned_data['comment']
                                             )
        status = StatusAdd.objects.get(name=self.cleaned_data['status'])
        Status.objects.create(equipment=equipment, name=status)
        Tag.objects.create(equipment=equipment, name=tag)
        Location.objects.create(equipment=equipment, name=location)
        GP.objects.get_or_create(name=position)
        Position.objects.create(equipment=equipment, name=position)
        Description.objects.create(equipment=equipment, user=user, name=description)

        return self.cleaned_data


class AddDeviceForm(forms.Form):
    serial_number = forms.CharField(label='Серийный номер', max_length=255,
                                    widget=forms.TextInput(attrs={'class': 'type2'}))
    model = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}),
                                   queryset=EquipmentModel.objects.all(),
                                   label='Модель', required=False, )
    model_new = forms.CharField(label='Добавить модель:', widget=forms.TextInput(attrs={'class': 'type2'}),
                                required=False)
    # type = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}), label='Тип оборудования:',
    #                               queryset=EquipmentType.objects.all(), required=False)
    # type_new = forms.CharField(label='Добавить тип:', max_length=255, widget=forms.TextInput(attrs={'class': 'type2'}),
    #                            required=False)
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
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'type2'}), required=False, label='Примечание:')
    position = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}), queryset=GP.objects.all(),
                                      label='Поз. по ГП', required=False)
    position_new = forms.CharField(widget=forms.TextInput(attrs={'class': 'type2'}),
                                   label='Добавить позицию по ГП:', max_length=255, required=False)
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'type2'}), max_length=50, required=False,
                               label='Место установки:')
    tag = forms.CharField(label='Тег', widget=forms.TextInput(attrs={'class': 'type2'}), max_length=255)
    status = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}), queryset=StatusAdd.objects.all(),
                                    label='Статус', required=False)
    status_new = forms.CharField(label='Добавить статус', max_length=255,
                                 widget=forms.TextInput(attrs={'class': 'type2'}), required=False)
    year = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}), label='Год выпуска:',
                                  queryset=Year.objects.all(), required=False)
    # reg_number = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}), label='Регистрационный номер:',
    #                                     queryset=RegNumber.objects.all(),
    #                                     required=False)
    # reg_number_new = forms.CharField(widget=forms.TextInput(attrs={'class': 'type2'}),
    #                                  label='Добавить регистрационный номер:', max_length=255, required=False)
    # previous_verification = forms.DateField(label='Дата предыдущей поверки:', required=False, widget=forms.TextInput(attrs=
    # {
    #     'type': 'date',
    #     'class': 'owner',
    # }))
    # certificate = forms.CharField(widget=forms.TextInput(attrs={"class": "type2"}), label='Сертификат:')
    interval = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select'}), label='Межповерочный интервал:',
                                 choices=CHOICES_INTERVAL)
    min_scale = forms.DecimalField(widget=forms.TextInput(attrs={"class": "type2"}), label='Мин. шкалы:')
    max_scale = forms.DecimalField(widget=forms.TextInput(attrs={"class": "type2"}), label='Макс. шкалы:')
    unit = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}),
                                  label='Единицы измерения:', queryset=Unit.objects.all(), required=False)
    unit_new = forms.CharField(widget=forms.TextInput(attrs={'class': 'type2'}), label='Довавить ЕИ', required=False)

    def clean(self):
        if Equipment.objects.filter(serial_number=self.cleaned_data['serial_number'],
                                    model=self.cleaned_data['model']):
            raise forms.ValidationError(message='Оборудование уже есть.')
        if (self.cleaned_data['model'] is None) & (self.cleaned_data['model_new'] == ''):
            raise forms.ValidationError(message='Не указана модель.')
        if self.cleaned_data['tag'] == '':
            self.cleaned_data['tag'] = ' '
        if len(self.cleaned_data['model_new']) > 255:
            raise forms.ValidationError(message='Модель должен быть до 255 символов.')
        if (self.cleaned_data['manufacturer'] is None) & (self.cleaned_data['manufacturer_new'] == ''):
            raise forms.ValidationError(message='Не указан производитель.')
        if len(self.cleaned_data['manufacturer_new']) > 255:
            raise forms.ValidationError(message='Производитель должен быть до 255 символов.')
        if (self.cleaned_data['name'] is None) & (self.cleaned_data['name_new'] == ''):
            raise forms.ValidationError(message='Не указано наименование.')
        if len(self.cleaned_data['name_new']) > 255:
            raise forms.ValidationError(message='Наименование должно быть до 255 символов')
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
        # if (self.cleaned_data['type'] is None) & (self.cleaned_data['type_new'] == ''):
        #     raise forms.ValidationError(message='Не указан тип оборудования.')
        # if (self.cleaned_data['reg_number'] is None) & (self.cleaned_data['reg_number_new'] == ''):
        #     raise forms.ValidationError(message='Не указан регистрационный номер.')
        # if self.cleaned_data['type_new']:
        #     self.cleaned_data['type'] = self.cleaned_data['type_new']
        if self.cleaned_data['manufacturer_new']:
            self.cleaned_data['manufacturer'] = self.cleaned_data['manufacturer_new']
        if self.cleaned_data['name_new']:
            self.cleaned_data['name'] = self.cleaned_data['name_new']
        if self.cleaned_data['model_new']:
            self.cleaned_data['model'] = self.cleaned_data['model_new']
        if self.cleaned_data['status_new']:
            self.cleaned_data['status'] = self.cleaned_data['status_new']
        # if self.cleaned_data['reg_number_new']:
        #     self.cleaned_data['reg_number'] = self.cleaned_data['reg_number_new']
        if self.cleaned_data['unit_new']:
            self.cleaned_data['unit'] = self.cleaned_data['unit_new']
        if (self.cleaned_data['unit_new'] == '') and (self.cleaned_data['unit'] is None):
            raise forms.ValidationError(message='Не указаны единицы измерения')
        if self.cleaned_data['position_new']:
            self.cleaned_data['position'] = self.cleaned_data['position_new']
        if (self.cleaned_data['position_new'] == '') and (self.cleaned_data['position'] is None):
            raise forms.ValidationError(message='Не указана позиция по ГП')
        if Equipment.objects.filter(
                Q(serial_number=self.cleaned_data['serial_number']) & Q(model__name=self.cleaned_data['model'])):
            raise forms.ValidationError(message='Оборудование уже есть.')
        return self.cleaned_data

    def save(self, user):
        description = self.cleaned_data.pop('description')
        location = self.cleaned_data.pop('location')
        tag = self.cleaned_data.pop('tag')
        min_scale = self.cleaned_data.pop('min_scale')
        max_scale = self.cleaned_data.pop('max_scale')
        position = self.cleaned_data.pop('position')
        # if self.cleaned_data['previous_verification']:
        #     previous_verification = self.cleaned_data.pop('previous_verification')
        # else:
        previous_verification = datetime.date.fromisoformat('1990-01-01')
        # certificate = self.cleaned_data.pop('certificate')
        # EquipmentType.objects.get_or_create(name=self.cleaned_data['type'])
        Manufacturer.objects.get_or_create(name=self.cleaned_data['manufacturer'])
        EquipmentName.objects.get_or_create(name=self.cleaned_data['name'])
        EquipmentModel.objects.get_or_create(name=self.cleaned_data['model'])
        StatusAdd.objects.get_or_create(name=self.cleaned_data['status'])
        GP.objects.get_or_create(name=position)
        equipment = Equipment.objects.create(serial_number=self.cleaned_data['serial_number'],
                                             # type=EquipmentType.objects.get(name=self.cleaned_data['type']),
                                             manufacturer=Manufacturer.objects.get(
                                                 name=self.cleaned_data['manufacturer']),
                                             name=EquipmentName.objects.get(name=self.cleaned_data['name']),
                                             model=EquipmentModel.objects.get(name=self.cleaned_data['model']),
                                             year=Year.objects.get(name=self.cleaned_data['year'].name),
                                             comment=self.cleaned_data['comment']
                                             )
        status = StatusAdd.objects.get(name=self.cleaned_data['status'])
        Status.objects.create(equipment=equipment, name=status)
        Tag.objects.create(equipment=equipment, name=tag)
        Location.objects.create(equipment=equipment, name=location)
        GP.objects.get_or_create(name=position)
        Position.objects.create(equipment=equipment, name=position)
        Description.objects.create(equipment=equipment, user=user, name=description)
        VerificationInterval.objects.get_or_create(name=self.cleaned_data['interval'])
        Scale.objects.get_or_create(min_scale=min_scale, max_scale=max_scale)
        # Error.objects.get_or_create(name=self.cleaned_data['error'])
        # RegNumber.objects.get_or_create(name=self.cleaned_data['reg_number'])
        Unit.objects.get_or_create(name=self.cleaned_data['unit'])
        Si.objects.create(equipment=equipment,
                          previous_verification=previous_verification,
                          next_verification=previous_verification + relativedelta(
                              months=+(int(self.cleaned_data['interval']))),
                          # certificate=certificate,
                          interval=VerificationInterval.objects.get(name=self.cleaned_data['interval']),
                          scale=Scale.objects.get(min_scale=min_scale, max_scale=max_scale),
                          unit=Unit.objects.get(name=self.cleaned_data['unit']))
        # error_device=Error.objects.get(name=self.cleaned_data['error']),
        # reg_number=RegNumber.objects.get(name=self.cleaned_data['reg_number']))
        return self.cleaned_data


class SearchForm(forms.Form):
    serial_number = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))


class DraftForm(forms.ModelForm):
    serial_number_draft = forms.CharField(label='Серийный номер', max_length=255,
                                          widget=forms.TextInput(attrs={'class': 'type2'}))
    model_draft = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}),
                                         queryset=EquipmentModel.objects.all(),
                                         label='Модель')
    name_draft = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}),
                                        queryset=EquipmentName.objects.all(),
                                        label='Наименование')
    min_scale_draft = forms.DecimalField(widget=forms.TextInput(attrs={"class": "type2"}), label='Мин. шкалы:')
    max_scale_draft = forms.DecimalField(widget=forms.TextInput(attrs={"class": "type2"}), label='Макс. шкалы:')
    year_draft = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}), label='Год выпуска:',
                                        queryset=Year.objects.all())
    unit_draft = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}),
                                        queryset=Unit.objects.all(),
                                        label='Единица измерения')
    manufacturer_draft = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}),
                                                queryset=Manufacturer.objects.all(),
                                                label='Производитель')
    poz_draft = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}), queryset=GP.objects.all(),
                                       label='Поз. по ГП', required=True)
    # poz_draft_new = forms.CharField(widget=forms.TextInput(attrs={'class': 'type2'}),
    #                                 label='Добавить позицию по ГП:', max_length=20, required=False)
    location_draft = forms.CharField(widget=forms.TextInput(attrs={'class': 'type2'}), label='Расположение')
    description_draft = forms.CharField(
        widget=forms.Textarea(attrs={"class": "type2"}), label='Комментарий:')
    tag_draft = forms.CharField(widget=forms.TextInput(attrs={'class': 'type2'}), label='Тэг:', required=True)
    status_draft = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}),
                                          queryset=StatusAdd.objects.all(),
                                          label='Статус')
    images = forms.ImageField(widget=forms.FileInput(attrs={'class': 'select'}))

    # def clean(self):
    #     cleaned_data = super(DraftForm, self).clean()
    #     if cleaned_data['poz_draft_new']:
    #         cleaned_data['poz_draft'] = cleaned_data['']
    #     return cleaned_data
    # def clean(self):
    # if self.cleaned_data['poz_draft_new']:
    #     self.cleaned_data['poz_draft'] = self.cleaned_data['poz_draft_new']
    # if (self.cleaned_data['poz_draft_new'] == '') and (self.cleaned_data['poz_draft'] is None):
    #     raise forms.ValidationError(message='Не указана позиция по ГП')

    class Meta(object):
        model = Draft
        fields = ['serial_number_draft', 'model_draft', 'name_draft', 'manufacturer_draft', 'poz_draft',
                  'location_draft', 'description_draft', 'tag_draft', 'year_draft', 'status_draft', 'min_scale_draft',
                  'max_scale_draft', 'unit_draft', 'images']


class DraftFormDevice(forms.Form):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': '4', 'cols': '80'}))


# class FormFilter(forms.Form):
#     search = forms.ModelChoiceField(queryset=EquipmentType.objects.all())


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User name'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class MyExamsForm(forms.Form):
    exams_ot = forms.DateField(widget=forms.TextInput(attrs={'type': 'date',
                                                             'class': 'type2'}), label='Охрана труда')
    exams_eb = forms.DateField(widget=forms.TextInput(attrs={'type': 'date',
                                                             'class': 'type2'}), label='Эл. безопасность')

    def save(self, user):
        my_exam = MyExam.objects.filter(user=user)
        if not my_exam:
            exams = MyExam(user=user, exams_ot=self.cleaned_data['exams_ot'], exams_eb=self.cleaned_data['exams_eb'])
            exams.save()
        else:
            exams = MyExam.objects.get(user=user)
            exams.exams_ot = self.cleaned_data['exams_ot']
            exams.exams_eb = self.cleaned_data['exams_eb']
            exams.save()
        return self.cleaned_data


#
class PprForm(forms.Form):
    name = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}),
                                  queryset=GP.objects.all(),
                                  label='Поз. по гп')
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'type2'}), label='Характер работ')
    required_materials = forms.CharField(widget=forms.Textarea(attrs={'class': 'type2'}), label='Необходимые материалы')

    class Meta(object):
        model = PprPlan
        fields = ['name', 'description', 'required_materials', ]

    def save(self, user, pk):
        pp = PprDate.objects.get(pk=pk)
        PprPlan.objects.create(ppr=pp,
                               name=self.cleaned_data['name'],
                               description=self.cleaned_data['description'],
                               required_materials=self.cleaned_data['required_materials'],
                               user=user
                               )
        return self.cleaned_data

#
# class PprUpdateForm(forms.ModelForm):
#     date_start = forms.CharField(widget=forms.TextInput(attrs={'class': 'type2'}))
#
#     class Meta:
#         model = Ppr
#         fields = ['date_start','name', 'description', 'required_materials', ]
#
#
# class PprDateForm(PprUpdateForm):
#     date_ppr = forms.CharField(widget=forms.TextInput(attrs={'class': 'type2'}))
#     name = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'select'}),
#                                   queryset=GP.objects.all())
#     description = forms.CharField(widget=forms.Textarea(attrs={'rows': '4', 'cols': '80'}))
#     required_materials = forms.CharField(widget=forms.Textarea(attrs={'rows': '4', 'cols': '80'}))
#
#     class Meta():
#         model = PprDate
#         fields = ['name', 'description', 'required_materials', 'date_start']


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")