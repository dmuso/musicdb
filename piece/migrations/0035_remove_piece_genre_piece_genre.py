# Generated by Django 4.1.5 on 2023-01-14 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('piece', '0034_alter_piece_isbn'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='piece',
            name='genre',
        ),
        migrations.AddField(
            model_name='piece',
            name='genre',
            field=models.ManyToManyField(blank=True, to='piece.genre'),
        ),
    ]
