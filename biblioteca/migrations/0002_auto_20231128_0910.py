# Generated by Django 3.2.23 on 2023-11-28 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='direccion',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='dni',
            field=models.CharField(max_length=9, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='telefono',
            field=models.IntegerField(null=True),
        ),
    ]