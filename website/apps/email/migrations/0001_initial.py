# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-17 19:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DoNotSendEmailList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.TextField(default=None)),
                ('notes', models.TextField(blank=True)),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True)),
                ('last_modified_timestamp', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['last_modified_timestamp'],
                'get_latest_by': 'last_modified_timestamp',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_recipient', models.TextField(default=None)),
                ('from_address', models.TextField(default=None)),
                ('email_subject', models.TextField(default=None)),
                ('email_body', models.TextField(default=None)),
                ('tracking_code', models.TextField(blank=True, default=None, null=True)),
                ('status', models.TextField(choices=[(b'Unsent', b'Unsent'), (b'Failed', b'Failed'), (b'Sent', b'Sent')], default=b'Unsent')),
                ('sent_timestamp', models.DateTimeField(blank=True, default=None, null=True)),
                ('last_error_message', models.TextField(blank=True, null=True)),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True)),
                ('last_modified_timestamp', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Email',
                'db_table': 'email',
                'managed': True,
                'verbose_name_plural': 'Emails',
            },
        ),
    ]
