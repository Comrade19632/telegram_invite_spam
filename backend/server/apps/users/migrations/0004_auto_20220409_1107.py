# Generated by Django 3.1.2 on 2022-04-09 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_auto_20220409_1059"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                blank=True, max_length=128, null=True, verbose_name="username"
            ),
        ),
    ]