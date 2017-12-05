# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-05 07:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scaner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('social_id', models.CharField(max_length=250)),
                ('name', models.CharField(max_length=250)),
                ('surname', models.CharField(max_length=250)),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
