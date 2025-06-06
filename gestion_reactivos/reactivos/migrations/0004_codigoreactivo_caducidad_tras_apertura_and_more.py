# Generated by Django 5.2.1 on 2025-05-19 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reactivos', '0003_delete_salida'),
    ]

    operations = [
        migrations.AddField(
            model_name='codigoreactivo',
            name='caducidad_tras_apertura',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='codigoreactivo',
            name='categoria',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='codigoreactivo',
            name='codigo',
            field=models.IntegerField(unique=True),
        ),
    ]
