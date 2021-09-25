# Generated by Django 3.2.7 on 2021-09-25 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('piece', '0006_auto_20210925_0655'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstrumentGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=240)),
                ('abbreviation', models.CharField(max_length=2)),
            ],
        ),
        migrations.AddField(
            model_name='instrument',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='piece.instrumentgroup'),
            preserve_default=False,
        ),
    ]
