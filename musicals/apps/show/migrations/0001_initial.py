# Generated by Django 5.1.3 on 2025-01-15 08:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShowType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='공연분류')),
            ],
            options={
                'db_table': 'show_showtype',
            },
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='공연명')),
                ('start_date', models.DateField(verbose_name='공연 시작일')),
                ('end_date', models.DateField(verbose_name='공연 종료일')),
                ('stadium', models.CharField(verbose_name='공연장소')),
                ('show_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='show.showtype')),
            ],
            options={
                'db_table': 'show_show',
            },
        ),
    ]
