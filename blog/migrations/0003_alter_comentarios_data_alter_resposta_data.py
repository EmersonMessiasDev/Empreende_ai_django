# Generated by Django 4.2.1 on 2023-06-01 01:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_comentarios_comentario_pai_resposta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentarios',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 1, 1, 44, 39, 457693, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='resposta',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 1, 1, 44, 39, 458046, tzinfo=datetime.timezone.utc)),
        ),
    ]