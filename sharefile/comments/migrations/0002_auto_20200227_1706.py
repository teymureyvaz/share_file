# Generated by Django 3.0.3 on 2020-02-27 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='owner_id',
            new_name='author',
        ),
    ]