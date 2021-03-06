# Generated by Django 3.1.2 on 2022-04-27 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0006_inviteorder_in_progress"),
    ]

    operations = [
        migrations.AlterField(
            model_name="inviteorder",
            name="in_progress",
            field=models.BooleanField(
                db_index=True, default=False, verbose_name="В процессе выполнения?"
            ),
        ),
    ]
