# Generated by Django 4.2.10 on 2024-03-11 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('biblio_app', '0005_multa_actualiz_alter_multa_alumno_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='multa',
            name='prestamo',
        ),
    ]
