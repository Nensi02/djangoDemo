# Generated by Django 5.0.6 on 2024-05-11 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_app', '0004_alter_services_modified_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]