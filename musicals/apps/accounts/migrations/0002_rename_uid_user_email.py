# Generated by Django 5.1.3 on 2025-01-13 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='uid',
            new_name='email',
        ),
    ]
