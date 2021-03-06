# Generated by Django 3.2.7 on 2021-09-25 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('piece', '0014_auto_20210925_0739'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='composer',
            options={'ordering': ['last_name', 'first_name']},
        ),
        migrations.RenameField(
            model_name='composer',
            old_name='name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='composer',
            name='last_name',
            field=models.CharField(default='Blank', max_length=240),
            preserve_default=False,
        ),
    ]
