# Generated by Django 4.2.13 on 2024-05-29 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='change_details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('process', 'In Process'), ('review', 'Review'), ('change_request', 'Change Request'), ('complete', 'Complete')], default='pending', max_length=200),
        ),
    ]
