# Generated by Django 4.0.4 on 2022-05-20 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClearanceRequests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_on', models.DateTimeField(auto_created=True, verbose_name='Date of Request')),
                ('status', models.IntegerField(choices=[(0, 'Submitted'), (1, 'Review'), (2, 'Cleared')], default=0, verbose_name='Status')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.student')),
            ],
            options={
                'verbose_name': 'Request',
                'verbose_name_plural': 'Requests',
            },
        ),
        migrations.CreateModel(
            name='ControlNumbers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_created=True, verbose_name='Student')),
                ('control_no', models.IntegerField(verbose_name='Control Number')),
                ('amount', models.IntegerField(verbose_name='Amount Payable')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clearance.clearancerequests')),
            ],
            options={
                'verbose_name': 'Control Number',
                'verbose_name_plural': 'Control Numbers',
            },
        ),
    ]
