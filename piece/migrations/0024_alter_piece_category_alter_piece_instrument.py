# Generated by Django 4.0.3 on 2022-04-18 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('piece', '0023_alter_piece_accompaniment_alter_piece_arrangers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piece',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='old_category', to='piece.category'),
        ),
        migrations.AlterField(
            model_name='piece',
            name='instrument',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='old_instrument', to='piece.instrument'),
        ),
    ]
