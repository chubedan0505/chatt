# Generated by Django 4.2.5 on 2024-01-09 06:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0017_alter_confirmationcode_expiration_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="confirmationcode",
            name="expiration_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 1, 10, 6, 14, 56, 794250, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
