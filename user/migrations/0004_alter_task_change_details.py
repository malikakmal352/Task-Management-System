# Generated by Django 4.2.13 on 2024-05-28 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_task_change_details_alter_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='change_details',
            field=models.TextField(blank=True, null=True),
        ),
    ]
