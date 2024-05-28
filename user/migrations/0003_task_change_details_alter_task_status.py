# Generated by Django 4.2.13 on 2024-05-28 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_task_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='change_details',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('process', 'In Process'), ('review', 'Review'), ('change_request', 'Change Request'), ('complete', 'Complete')], default='pending', max_length=200),
        ),
    ]