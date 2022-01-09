# Generated by Django 3.0.1 on 2021-01-25 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('COVID_19_Tracker', '0013_auto_20210123_2338'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountryCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iso', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=1000)),
            ],
        ),
    ]
