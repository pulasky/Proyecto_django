# Generated by Django 5.2.1 on 2025-05-20 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reactivos', '0004_codigoreactivo_caducidad_tras_apertura_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='caducidadporcategoria',
            name='reactivo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='caducidadporcategoria',
            name='caducidad_tras_apertura',
            field=models.CharField(help_text='Caducidad tras apertura', max_length=100),
        ),
    ]
