# Generated by Django 4.2.10 on 2024-05-22 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblio_app', '0006_remove_multa_prestamo'),
    ]

    operations = [
        migrations.CreateModel(
            name='LastUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
