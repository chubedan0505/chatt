# Generated by Django 4.2.5 on 2024-01-19 08:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0022_alter_confirmationcode_expiration_date_message"),
    ]

    operations = [
        migrations.AlterField(
            model_name="confirmationcode",
            name="expiration_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 1, 19, 8, 13, 44, 948730, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]