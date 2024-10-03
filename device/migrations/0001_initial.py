# Generated by Django 5.0.6 on 2024-10-02 17:31

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Approve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='ФИО утв.')),
                ('job_title', models.CharField(max_length=50, verbose_name='Должность')),
                ('organization', models.CharField(max_length=100, verbose_name='Организация')),
            ],
            options={
                'verbose_name_plural': 'Утверждающие',
            },
        ),
        migrations.CreateModel(
            name='Contractor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='ФИО подряднчика')),
                ('job_title', models.CharField(max_length=50, verbose_name='Должность')),
                ('organization', models.CharField(max_length=100, verbose_name='Организация')),
            ],
            options={
                'verbose_name_plural': 'Подрядные организации',
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=25, verbose_name='Серийный номер')),
                ('at_date', models.DateField(auto_now_add=True, verbose_name='Дата добавления')),
                ('defect', models.BooleanField(blank=True, default=False, null=True)),
                ('si_or', models.BooleanField(default=True, verbose_name='Средство измерения')),
            ],
            options={
                'verbose_name_plural': 'Оборудование',
                'ordering': ('-at_date',),
            },
        ),
        migrations.CreateModel(
            name='EquipmentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Модель оборудования')),
            ],
            options={
                'verbose_name_plural': 'Модели оборудования',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='EquipmentName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Наименование оборудования')),
            ],
            options={
                'verbose_name_plural': 'Наименование оборудования',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='EquipmentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Тип оборудования')),
            ],
            options={
                'verbose_name_plural': 'Типы оборудования',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='GP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Позиция по ГП')),
                ('construction', models.CharField(blank=True, max_length=100, verbose_name='Наименование здания, сооружения')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Kait',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='ФИО мастера Каит')),
                ('job_title', models.CharField(max_length=50, verbose_name='Должность')),
                ('organization', models.CharField(max_length=100, verbose_name='Организация')),
            ],
            options={
                'verbose_name_plural': 'Мастера КАиТ',
                'ordering': ('-job_title',),
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Производитель оборудования')),
            ],
            options={
                'verbose_name_plural': 'Производители',
            },
        ),
        migrations.CreateModel(
            name='RegNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='Регистрационный номер')),
            ],
        ),
        migrations.CreateModel(
            name='Scale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_scale', models.CharField(max_length=10, verbose_name='Минимум шкалы')),
                ('max_scale', models.CharField(max_length=10, verbose_name='Максимум шкалы')),
            ],
        ),
        migrations.CreateModel(
            name='StatusAdd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Статус')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='Единицы измерения')),
            ],
        ),
        migrations.CreateModel(
            name='VerificationInterval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=4, verbose_name='Межповерочный интервал')),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='ФИО мастера цеха')),
                ('job_title', models.CharField(max_length=100, verbose_name='Должность')),
                ('organization', models.CharField(max_length=100, verbose_name='Организация')),
            ],
            options={
                'verbose_name_plural': 'Мастера цеха',
            },
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(2045), django.core.validators.MinValueValidator(2020)], verbose_name='Год выпуска')),
            ],
        ),
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Описание')),
                ('at_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='descriptions', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='descriptions', to='device.equipment', verbose_name='Описание оборудования')),
            ],
            options={
                'verbose_name_plural': 'Описания оборудования',
            },
        ),
        migrations.AddField(
            model_name='equipment',
            name='model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='model', to='device.equipmentmodel'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='n', to='device.equipmentname', verbose_name='Наименование оборудования'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='type',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='type', to='device.equipmenttype', verbose_name='Тип'),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Место нахождения.')),
                ('equipment', models.ForeignKey(default='NoneLocation', on_delete=django.db.models.deletion.DO_NOTHING, related_name='locations', to='device.equipment', verbose_name='Место установки')),
            ],
            options={
                'verbose_name_plural': 'Места установки',
            },
        ),
        migrations.AddField(
            model_name='equipment',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manufacturer', to='device.manufacturer', verbose_name='Производитель'),
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, null=True, verbose_name='Позиция по ГП')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='positions', to='device.equipment')),
            ],
            options={
                'verbose_name_plural': 'Позиции',
                'ordering': ('-equipment',),
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='status', to='device.equipment', verbose_name='Статус')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='statuses', to='device.statusadd', verbose_name='Статус')),
            ],
            options={
                'ordering': ('equipment',),
            },
        ),
        migrations.CreateModel(
            name='Draft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_draft', models.CharField(max_length=150, verbose_name='Место установки')),
                ('tag_draft', models.CharField(max_length=150, verbose_name='Тэг')),
                ('description_draft', models.CharField(max_length=150, verbose_name='Описание')),
                ('images', models.ImageField(upload_to='images', verbose_name='Фото')),
                ('user_draft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('poz_draft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='device.gp', verbose_name='Поз. по ГП')),
                ('status_draft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='device.statusadd', verbose_name='Статус')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Тэг')),
                ('equipment', models.ForeignKey(default='NoneTag', on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='device.equipment', verbose_name='Тэг')),
            ],
            options={
                'verbose_name_plural': 'Тэг',
            },
        ),
        migrations.CreateModel(
            name='Si',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('previous_verification', models.DateField(verbose_name='Дата предыдущей поверки')),
                ('next_verification', models.DateField(verbose_name='Дата следующей поверки')),
                ('certificate', models.CharField(default='еще нет', max_length=100, verbose_name='Свидетельство о поверке')),
                ('result', models.BooleanField(default=True)),
                ('com', models.TextField(default='none', verbose_name='Комментарий')),
                ('equipment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='si', to='device.equipment', verbose_name='Средство измерения')),
                ('reg_number', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='reg_number', to='device.regnumber', verbose_name='Регистрационный номер')),
                ('scale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scale', to='device.scale', verbose_name='Шкала датчика')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unit', to='device.unit', verbose_name='Единица измерения')),
                ('interval', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interval', to='device.verificationinterval', verbose_name='Межповерочный интервал (мес)')),
            ],
            options={
                'verbose_name_plural': 'Средства измерения',
            },
        ),
        migrations.CreateModel(
            name='Defect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('defect_act', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Номер деффектного акта')),
                ('project', models.CharField(max_length=100, verbose_name='Наименование проекта')),
                ('short_description', models.TextField(verbose_name='Краткое описание деффекта')),
                ('causes', models.TextField(verbose_name='Причина отказа')),
                ('operating_time', models.SmallIntegerField(verbose_name='Время наработки')),
                ('invest_letter', models.CharField(max_length=255, verbose_name='Номер письма в Инвест')),
                ('approve', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='approve', to='device.approve', verbose_name='Утверждающий')),
                ('contractor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='contractor', to='device.contractor', verbose_name='Подрядчик')),
                ('defect', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='equipment', to='device.equipment')),
                ('kait', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='kait', to='device.kait', verbose_name='Мастер по КАиТ')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='worker', to='device.worker', verbose_name='Мастер цеха')),
            ],
        ),
        migrations.AddField(
            model_name='equipment',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='years', to='device.year', verbose_name='Год выпуска'),
        ),
        migrations.AlterUniqueTogether(
            name='equipment',
            unique_together={('serial_number', 'model')},
        ),
    ]
