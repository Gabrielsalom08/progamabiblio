# Generated by Django 5.0.1 on 2024-01-31 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblio_app', '0002_prestamo_multa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prestamo',
            name='fecha_regreso',
            field=models.DateField(blank=True, null=True),
        ),
    ]
