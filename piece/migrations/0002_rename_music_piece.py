# Generated by Django 3.2.7 on 2021-09-25 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instrument', '0001_initial'),
        ('piece', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Music',
            new_name='Piece',
        ),
    ]
