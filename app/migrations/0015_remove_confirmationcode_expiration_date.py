# Generated by Django 4.2.5 on 2024-01-08 05:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0014_confirmationcode_expiration_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="confirmationcode",
            name="expiration_date",
        ),
    ]