# Generated by Django 2.0.3 on 2018-03-26 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='create_time',
            new_name='createed_time',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='modified',
            new_name='modified_time',
        ),
    ]