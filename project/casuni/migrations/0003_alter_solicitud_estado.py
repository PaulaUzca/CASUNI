# Generated by Django 4.2.13 on 2024-07-07 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('casuni', '0002_alter_estudiante_imagen_alter_fotoalojamiento_imagen_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='estado',
            field=models.CharField(choices=[('P', 'Pendiente'), ('A', 'Aceptada'), ('R', 'Rechazada')], default='P', max_length=10),
        ),
    ]
