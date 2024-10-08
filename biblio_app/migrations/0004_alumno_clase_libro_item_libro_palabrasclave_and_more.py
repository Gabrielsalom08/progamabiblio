# Generated by Django 4.2.10 on 2024-02-22 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblio_app', '0003_alter_prestamo_fecha_regreso'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumno',
            name='clase',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='libro',
            name='item',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
        migrations.AddField(
            model_name='libro',
            name='palabrasclave',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='prestamo',
            name='fecha_creacion',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='libro',
            name='autor',
            field=models.CharField(max_length=240),
        ),
    ]
