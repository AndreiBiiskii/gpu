import datetime
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import PROTECT
from django.urls import reverse


class StatusAdd(models.Model):
    name = models.CharField(max_length=255, verbose_name='Статус', unique=True)

    def __str__(self):
        return self.name

    # class Meta:
    #     ordering = ['-name']


class Status(models.Model):
    name = models.ForeignKey(StatusAdd, on_delete=models.DO_NOTHING, related_name='statuses', verbose_name='Статус')
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE, related_name='status',
                                  verbose_name='Статус')

    def __str__(self):
        return self.equipment

    class Meta:
        ordering = ['id']


class VerificationInterval(models.Model):
    name = models.CharField(max_length=4, verbose_name='Межповерочный интервал')

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, verbose_name='Производитель оборудования', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Производители'
        ordering = ['name']


# class EquipmentType(models.Model):
#     name = models.CharField(max_length=255, verbose_name='Тип оборудования', unique=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name_plural = 'Типы оборудования'
#         ordering = ['name']


class EquipmentModel(models.Model):
    name = models.CharField(max_length=255, verbose_name='Модель оборудования', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Модели оборудования'
        ordering = ['name']


class EquipmentName(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование оборудования', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Наименование оборудования'
        ordering = ['name']


class Position(models.Model):
    name = models.CharField(verbose_name='Позиция по ГП', blank=True, null=True)
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE, related_name='positions')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Позиции'
        ordering = ['id']


class Description(models.Model):
    name = models.TextField(verbose_name='Описание', blank=False, null=False)
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE, verbose_name='Описание оборудования',
                                  related_name='descriptions')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='descriptions',
                             verbose_name='Пользователь')
    at_date = models.DateTimeField(auto_now=True, verbose_name='Дата добавления')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Описания оборудования'
        ordering = ['id']


class Location(models.Model):
    name = models.CharField(max_length=255, verbose_name='Место нахождения.', blank=True, null=True)
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE, related_name='locations',
                                  verbose_name='Место установки', default='NoneLocation')

    def __str__(self):
        return self.equipment

    class Meta:
        verbose_name_plural = 'Места установки'
        ordering = ['id']


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='Тэг', blank=True, null=True)
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE, related_name='tags', verbose_name='Тэг',
                                  default='NoneTag')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Тэг'
        ordering = ['id']


class Files(models.Model):
    file = models.FileField(blank=True, null=True, upload_to='files')


class Equipment(models.Model):
    serial_number = models.CharField(max_length=255, verbose_name='Серийный номер')
    model = models.ForeignKey(EquipmentModel, on_delete=models.DO_NOTHING, related_name='model', blank=True, null=True)
    at_date = models.DateTimeField(auto_now=True, verbose_name='Дата добавления')
    defect_or = models.BooleanField(default=False, blank=True, null=True, verbose_name='Дефектное')
    si_or = models.BooleanField(default=True, verbose_name='Средство измерения')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.DO_NOTHING, related_name='manufacturer',
                                     verbose_name='Производитель')
    # type = models.ForeignKey(EquipmentType, on_delete=models.DO_NOTHING, related_name='type',
    #                          verbose_name='Тип', default=None, null=True)
    name = models.ForeignKey(EquipmentName, on_delete=models.DO_NOTHING, related_name='n',
                             verbose_name='Наименование оборудования')
    year = models.ForeignKey('Year', on_delete=models.DO_NOTHING, related_name='years', verbose_name='Год выпуска')

    def __str__(self):
        return self.serial_number

    def get_absolute_url(self):
        return reverse('equipment_detail', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ('serial_number', 'model')
        verbose_name_plural = 'Оборудование'
        ordering = ['-name']


class Si(models.Model):
    equipment = models.ForeignKey(Equipment, blank=True, null=True, on_delete=models.CASCADE,
                                  related_name='si',
                                  verbose_name='Средство измерения')
    previous_verification = models.DateField(verbose_name='Дата предыдущей поверки', )
    next_verification = models.DateField(verbose_name='Дата следующей поверки')
    # certificate = models.CharField(max_length=255, verbose_name='Свидетельство о поверке', default='еще нет')
    interval = models.ForeignKey(VerificationInterval, on_delete=models.DO_NOTHING, related_name='interval', blank=True,
                                 null=True, verbose_name='Межповерочный интервал (мес)')
    scale = models.ForeignKey('Scale', on_delete=models.DO_NOTHING, related_name='scale', verbose_name='Шкала датчика')
    unit = models.ForeignKey('Unit', on_delete=models.DO_NOTHING, related_name='unit', verbose_name='Единица измерения')
    # error_device = models.ForeignKey('Error', on_delete=models.DO_NOTHING, related_name='error_device',
    #                                  verbose_name='Погрешность', default=1)
    # reg_number = models.ForeignKey('RegNumber', on_delete=models.DO_NOTHING, related_name='reg_number',
    #                                verbose_name='Регистрационный номер')
    result = models.BooleanField(default=True, )
    com = models.TextField(verbose_name='Комментарий', default='none')

    # def __str__(self):
    #     return self.equipment.name

    class Meta:
        verbose_name_plural = 'Средства измерения'

    # def get_absolute_url(self):
    #     return reverse('si_detail', kwargs={'pk': self.pk})


class Draft(models.Model):
    serial_number_draft = models.CharField(max_length=255, verbose_name='Серийный номер')
    model_draft = models.ForeignKey(EquipmentModel, on_delete=models.CASCADE, blank=False, null=False,
                                    verbose_name='Модель')
    manufacturer_draft = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, blank=False, null=False,
                                           verbose_name='Производитель')
    name_draft = models.ForeignKey(EquipmentName, on_delete=models.CASCADE, blank=False, null=False,
                                   verbose_name='Наименование')
    poz_draft = models.ForeignKey('GP', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Поз. по ГП')
    # poz_draft_new = models.CharField(max_length=255, verbose_name=' Новая позиция по ГП')
    location_draft = models.CharField(max_length=255, blank=False, null=False, verbose_name='Место установки')
    tag_draft = models.CharField(max_length=255, blank=False, null=False, verbose_name='Тэг')
    description_draft = models.TextField(blank=False, null=False, verbose_name='Описание')
    status_draft = models.ForeignKey(StatusAdd, on_delete=models.CASCADE, blank=False, null=False,
                                     verbose_name='Статус')
    images = models.ImageField(blank=False, null=False, verbose_name='Фото', upload_to='images')
    user_draft = models.ForeignKey(User, on_delete=models.CASCADE)
    min_scale_draft = models.CharField(max_length=255, verbose_name='Минимум шкалы')
    max_scale_draft = models.CharField(max_length=255, verbose_name='Максимум шкалы')
    unit_draft = models.ForeignKey('Unit', on_delete=models.CASCADE, verbose_name='Единица измерения')
    year_draft = models.ForeignKey('Year', on_delete=models.CASCADE, verbose_name='Год выпуска')

    def __str__(self):
        return self.poz_draft.name

    def get_absolute_url(self):
        return reverse('draft_detail', kwargs={'pk': self.pk})


class GP(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name='Позиция по ГП', unique=True)
    construction = models.CharField(max_length=255, blank=True, verbose_name='Наименование здания, сооружения')

    def __str__(self):
        return self.name

    # class Meta:
    #     ordering = ['-o', ]


# class RegNumber(models.Model):
#     name = models.CharField(max_length=255, unique=True, verbose_name='Регистрационный номер')
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         ordering = ['name', ]


# class Error(models.Model):
#     name = models.CharField(max_length=10, verbose_name='Погрешность')
#
#     def __str__(self):
#         return self.name


class Year(models.Model):
    name = models.SmallIntegerField(validators=[MaxValueValidator(2045), MinValueValidator(2020)],
                                    verbose_name='Год выпуска')

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['-name']


class Scale(models.Model):
    min_scale = models.CharField(max_length=255, verbose_name='Минимум шкалы')
    max_scale = models.CharField(max_length=255, verbose_name='Максимум шкалы')



class Unit(models.Model):
    name = models.CharField(max_length=255, verbose_name='Единицы измерения')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class MyExam(models.Model):
    user = models.ForeignKey(User, on_delete=PROTECT, verbose_name='Пользователь')
    exams_ot = models.DateField(verbose_name='Экзамет по ОТ')
    exams_eb = models.DateField(verbose_name='Экзамет по электоробезопасности')

    # at_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('id',)


class PprPlan(models.Model):
    ppr = models.ForeignKey('PprDate', related_name='ppr', on_delete=models.CASCADE, verbose_name='Период проведения')
    name = models.ForeignKey('GP', on_delete=models.CASCADE, null=False, blank=False, verbose_name='Поз. по ГП')
    description = models.TextField(verbose_name='Характер работ')
    user = models.ForeignKey(User, on_delete=PROTECT, verbose_name='Кто внес изменения')
    required_materials = models.TextField(verbose_name='Необходимые материалы', null=True, blank=True)
    at_date = models.DateField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return self.name.name

    def get_absolute_url(self):
        return reverse('ppr_update', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Проектные планы работ'
        ordering = ['-at_date']


class PprDate(models.Model):
    ppr_date = models.CharField(max_length=255, verbose_name='Период проведения', unique=True)
    at_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.ppr_date

    def get_absolute_url(self):
        return reverse('ppr_date_update', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Даты проведения ППР'
        ordering = ['-at_date']


class Manual(models.Model):
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория',
                                 related_name='categories')
    name = models.CharField(max_length=255, verbose_name='Наименование')
    file_full = models.FileField(upload_to='manuals/', verbose_name='Полное руководство')
    file_short = models.FileField(upload_to='manuals/', verbose_name='Подключение')
    file_short2 = models.FileField(upload_to='manuals/', verbose_name='Настройка')
    at_date = models.DateField(auto_now_add=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('manual_update', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Руководства'
        ordering = ['-name']


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Категория')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_update', kwargs={'pk': self.pk})
