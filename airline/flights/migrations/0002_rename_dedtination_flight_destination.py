# Generated by Django 3.2.4 on 2021-06-20 00:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flight',
            old_name='dedtination',
            new_name='destination',
        ),
    ]