from django.db import models
from django.urls import reverse

from device.models import Equipment


class Defect(models.Model):
    defect = models.ForeignKey(Equipment, blank=True, null=True, on_delete=models.DO_NOTHING, related_name='equipment')
    defect_act = models.CharField(max_length=20, verbose_name='Номер деффектного акта', blank=True, null=True,
                                  unique=True)
    project = models.CharField(max_length=100, verbose_name='Наименование проекта')
    short_description = models.TextField(verbose_name='Краткое описание деффекта')
    causes = models.TextField(verbose_name='Причина отказа')
    status = models.CharField(verbose_name='Статус')
    models.TextField(verbose_name='Что требуется для устранения')
    operating_time = models.SmallIntegerField(verbose_name='Время наработки')
    invest_letter = models.CharField(max_length=255, verbose_name='Номер письма в Инвест')
    approve = models.ForeignKey('Approve', on_delete=models.DO_NOTHING, related_name='approve',
                                verbose_name='Утверждающий')
    contractor = models.ForeignKey('Contractor', on_delete=models.DO_NOTHING, related_name='contractor',
                                   verbose_name='Подрядчик')
    kait = models.ForeignKey('Kait', on_delete=models.DO_NOTHING, related_name='kait', verbose_name='Мастер по КАиТ')
    worker = models.ForeignKey('Worker', on_delete=models.DO_NOTHING, related_name='worker', verbose_name='Мастер цеха')

    def get_absolute_url(self):
        return reverse('defect_detail', kwargs={'pk': self.pk})

class DefectAct(models.Model):
    defect_act = models.ForeignKey(Equipment, on_delete=models.DO_NOTHING, related_name='acts')


class Project(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование проекта')
    gp = models.CharField(max_length=100, verbose_name='ГП')
    year = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


#
# class DateCreate(models.Model):
#     name = models.DateField(verbose_name='Дата внесения записи дефекта')
#
#     # date_create = models.ForeignKey(Equipment, on_delete=models.DO_NOTHING, related_name='created')
#
#     def __str__(self):
#         return str(self.name)
#
#
# class ShortDescription(models.Model):
#     name = models.TextField(verbose_name='Краткое описание деффекта')
#     short_description = models.ForeignKey(Equipment, on_delete=models.DO_NOTHING, related_name='short_descriptions')
#
#     def __str__(self):
#         return self.name
#
#
# class Causes(models.Model):
#     name = models.TextField(verbose_name='Причина отказа')
#     causes = models.ForeignKey(Equipment, on_delete=models.DO_NOTHING, related_name='causes')
#
#     def __str__(self):
#         return self.name
#
#
# class Fix(models.Model):
#     name = models.TextField(verbose_name='Что требуется для устранения')
#     fix = models.ForeignKey(Equipment, on_delete=models.DO_NOTHING, related_name='fixes')
#
#     def __str__(self):
#         return self.name
#
#
# class OperatingTime(models.Model):
#     name = models.SmallIntegerField(verbose_name='Время наработки')
#     operating_time = models.ForeignKey(Equipment, on_delete=models.DO_NOTHING, related_name='operating_times')
#
#     def __str__(self):
#         return self.name
#
#
# class InvestLetter(models.Model):
#     name = models.CharField(max_length=255, verbose_name='Номер письма в Инвест')
#     invest_letter = models.ForeignKey(Equipment, on_delete=models.DO_NOTHING, related_name='invest_letters')
#
#     def __str__(self):
#         return self.name


class Approve(models.Model):
    name = models.CharField(max_length=30, verbose_name='ФИО утв.', unique=True)
    job_title = models.CharField(max_length=50, verbose_name='Должность')
    organization = models.CharField(max_length=100, verbose_name='Организация')

    # approve = models.ForeignKey(Equipment, on_delete=.DO_NOTHING, related_name='approves', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Утверждающие'


class Contractor(models.Model):
    name = models.CharField(max_length=30, verbose_name='ФИО подряднчика', unique=True)
    job_title = models.CharField(max_length=50, verbose_name='Должность')
    organization = models.CharField(max_length=100, verbose_name='Организация')

    # contractor = models.ForeignKey(Equipment, on_delete=models.DO_NOTHING, related_name='contractors', blank=True,
    # null = True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Подрядные организации'


class Kait(models.Model):
    name = models.CharField(max_length=30, verbose_name='ФИО мастера Каит', unique=True)
    job_title = models.CharField(max_length=50, verbose_name='Должность')
    organization = models.CharField(max_length=100, verbose_name='Организация')

    # kait = models.ForeignKey(Equipment, on_delete=models.DO_NOTHING, related_name='kaits', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Мастера КАиТ'
        ordering = ('-job_title',)


class Worker(models.Model):
    name = models.CharField(max_length=30, verbose_name='ФИО мастера цеха', unique=True)
    job_title = models.CharField(max_length=100, verbose_name='Должность')
    organization = models.CharField(max_length=100, verbose_name='Организация')

    # worker = models.ForeignKey(Equipment, on_delete=models.DO_NOTHING, related_name='workers', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Мастера цеха'
