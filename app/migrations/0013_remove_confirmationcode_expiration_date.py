# Generated by Django 4.2.5 on 2024-01-08 05:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0012_alter_confirmationcode_expiration_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="confirmationcode",
            name="expiration_date",
        ),
    ]
