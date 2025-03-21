from django.db import models
from django.urls import reverse

from device.models import Equipment


class Defect(models.Model):
    defect = models.ForeignKey(Equipment, on_delete=models.DO_NOTHING, related_name='equipment')
    model = models.CharField(max_length=255, verbose_name='Модель')
    name = models.CharField(max_length=255, verbose_name='Наименование', default='None')
    manufacture = models.CharField(max_length=255, verbose_name='Производитель')
    serial_number = models.CharField(max_length=100, verbose_name='Серийный номер')
    gp = models.CharField(max_length=50, verbose_name='Поз. по ГП')
    location = models.CharField(max_length=255, verbose_name='Место установки')
    tag = models.CharField(max_length=50, verbose_name='Тэг', blank=True)
    defect_act = models.CharField(max_length=50, verbose_name='Номер деффектного акта', blank=True, null=True,
                                  unique=True)
    project = models.CharField(max_length=100, verbose_name='Наименование проекта')
    short_description = models.TextField(verbose_name='Краткое описание деффекта')
    causes = models.TextField(verbose_name='Причина отказа')
    status = models.TextField(verbose_name='Статус')
    fix = models.TextField(verbose_name='Что требуется для устранения', default='None')
    operating_time = models.SmallIntegerField(verbose_name='Время наработки')
    invest_letter = models.CharField(max_length=255, verbose_name='Номер письма в Инвест')
    approve = models.ForeignKey('Approve', on_delete=models.DO_NOTHING, related_name='approve',
                                verbose_name='Утверждающий', blank=True, null=True)
    contractor = models.ForeignKey('Contractor', on_delete=models.DO_NOTHING, related_name='contractor',
                                   verbose_name='Мастер по КАиТ', )
    kait = models.ForeignKey('Kait', on_delete=models.DO_NOTHING, related_name='kait', verbose_name='Ст. мастер по КАиТ',
                             blank=True, null=True)
    worker = models.ForeignKey('Worker', on_delete=models.DO_NOTHING, related_name='worker', verbose_name='Мастер цеха',
                               blank=True, null=True)
    at_date = models.DateTimeField(auto_now=True, verbose_name='Дата добавления')

    def get_absolute_url(self):
        return reverse('defectone:defect_update', kwargs={'pk': self.pk})

    def str(self):
        return self.serial_number

    class Meta:
        verbose_name_plural = 'Дефекты'
        ordering = ['-at_date']


class Bid(models.Model):
    bid = models.ForeignKey(Equipment, on_delete=models.DO_NOTHING, related_name='bids')
    model = models.CharField(max_length=255, verbose_name='Модель')
    manufacture = models.CharField(max_length=255, verbose_name='Производитель')
    serial_number = models.CharField(max_length=100, verbose_name='Серийный номер')
    short_description = models.TextField(verbose_name='Краткое описание деффекта')


# class DefectAct(models.Model):
#     defect_act = models.ForeignKey(Equipment, on_delete=models.DO_NOTHING, related_name='acts')


class Projects(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование проекта')
    gp = models.CharField(max_length=100, verbose_name='ГП')
    year = models.DateField(blank=True)

    def __str__(self):
        return self.name


class Approve(models.Model):
    name = models.CharField(max_length=30, verbose_name='ФИО утв.', unique=True)
    job_title = models.CharField(max_length=50, verbose_name='Должность')
    organization = models.CharField(max_length=100, verbose_name='Организация')

    # approve = models.ForeignKey(Equipment, on_delete=.DO_NOTHING, related_name='approves', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('defectone:approve_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Утверждающие'


class Contractor(models.Model):
    name = models.CharField(max_length=30, verbose_name='ФИО подряднчика', unique=True)
    job_title = models.CharField(max_length=50, verbose_name='Должность')
    organization = models.CharField(max_length=100, verbose_name='Организация')

    # contractor = models.ForeignKey(Equipment, on_delete=models.DO_NOTHING, related_name='contractors', blank=True,
    # null = True)
    def get_absolute_url(self):
        return reverse('defectone:contractor_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Подрядные организации'


class Kait(models.Model):
    name = models.CharField(max_length=30, verbose_name='ФИО мастера Каит', unique=True)
    job_title = models.CharField(max_length=50, verbose_name='Должность')
    organization = models.CharField(max_length=100, verbose_name='Организация')

    # kait = models.ForeignKey(Equipment, on_delete=models.DO_NOTHING, related_name='kaits', blank=True, null=True)
    def get_absolute_url(self):
        return reverse('defectone:kait_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Мастера КАиТ'
        ordering = ('-job_title',)


class Worker(models.Model):
    name = models.CharField(max_length=30, verbose_name='ФИО слесаря', unique=True)
    job_title = models.CharField(max_length=100, verbose_name='Должность')
    organization = models.CharField(max_length=100, verbose_name='Организация')

    def get_absolute_url(self):
        return reverse('defectone:worker_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Слесарь'
