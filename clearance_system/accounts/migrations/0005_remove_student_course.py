# Generated by Django 4.0.4 on 2022-05-31 06:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_student_registrar_id_student_sponsor_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='course',
        ),
    ]