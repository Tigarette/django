# Generated by Django 4.0.5 on 2022-06-15 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('draw', '0002_alter_updatelog_log_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='updatelog',
            name='log_text',
            field=models.TextField(max_length=10000000),
        ),
    ]