# Generated by Django 3.2.7 on 2021-09-25 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('piece', '0009_publisher'),
    ]

    operations = [
        migrations.AddField(
            model_name='piece',
            name='publisher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='piece.publisher'),
            preserve_default=False,
        ),
    ]
