# Generated by Django 4.0.4 on 2022-05-23 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0002_alter_studentitems_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentitems',
            name='return_date',
            field=models.DateField(blank=True, null=True, verbose_name='Returned On'),
        ),
    ]