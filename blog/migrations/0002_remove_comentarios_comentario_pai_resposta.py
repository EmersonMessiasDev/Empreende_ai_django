# Generated by Django 4.2.1 on 2023-06-01 00:07

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autenticacao', '0001_initial'),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comentarios',
            name='comentario_pai',
        ),
        migrations.CreateModel(
            name='Resposta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('data', models.DateTimeField(default=datetime.datetime.now)),
                ('comentario_pai', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respostas', to='blog.comentarios')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autenticacao.usuario')),
            ],
        ),
    ]
