# Generated by Django 5.0.6 on 2024-05-11 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_app', '0003_alter_services_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
