# Generated by Django 4.1 on 2022-11-06 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("WePay", "0018_userprofile_display_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="display_name",
        ),
    ]
