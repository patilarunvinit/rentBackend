# Generated by Django 5.0.7 on 2024-07-27 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0006_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='b_date',
            field=models.DateField(null=True),
        ),
    ]