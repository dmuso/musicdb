# Generated by Django 4.0.3 on 2022-04-22 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('piece', '0025_piece_categories_piece_instruments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instrumentgroup',
            name='abbreviation',
        ),
    ]