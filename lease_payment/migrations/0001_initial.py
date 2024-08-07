# Generated by Django 5.0.7 on 2024-08-01 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='lease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner_id', models.IntegerField()),
                ('renter', models.IntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('rent', models.DecimalField(decimal_places=2, max_digits=10)),
                ('deposit', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
