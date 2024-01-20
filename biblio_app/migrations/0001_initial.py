# Generated by Django 5.0.1 on 2024-01-19 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('clave', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('grupo', models.CharField(max_length=5)),
                ('correo', models.CharField(blank=True, max_length=128, null=True)),
            ],
            options={
                'db_table': 'Alumnos',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
        ),
    ]
