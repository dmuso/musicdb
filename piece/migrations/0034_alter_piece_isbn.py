# Generated by Django 4.1.5 on 2023-01-14 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('piece', '0033_rename_category_shelflocation_alter_piece_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piece',
            name='isbn',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
