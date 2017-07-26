# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 22:32
from __future__ import unicode_literals

from lxml import etree
from lxml.etree import XMLSyntaxError
from django.db import migrations, models
from StringIO import StringIO

def convert_xml_name_property_to_name(apps, schema_editor):
    Scenario = apps.get_model("ts_om", "Scenario")
    for scenario in Scenario.objects.all():
        try:
            tree = etree.parse(StringIO(str(scenario.xml)))
        except XMLSyntaxError:
            name = "Invalid xml document"
        else:
            try:
                name = tree.getroot().xpath('@name')[0]
            except IndexError:
                name = "Unnamed scenario"
        scenario.name = name
        scenario.save()


class Migration(migrations.Migration):

    dependencies = [
        ('ts_om', 'load_fixtures'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenario',
            name='name',
            field=models.TextField(default=b''),
        ),
        migrations.RunPython(convert_xml_name_property_to_name),
    ]