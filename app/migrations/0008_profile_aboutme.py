# Generated by Django 4.2.5 on 2024-01-01 14:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0007_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="aboutme",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
