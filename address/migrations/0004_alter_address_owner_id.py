# Generated by Django 5.0.7 on 2024-07-30 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0003_address_owner_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='owner_id',
            field=models.IntegerField(null=True),
        ),
    ]
