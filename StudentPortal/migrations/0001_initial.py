# Generated by Django 4.2.7 on 2024-04-05 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=50)),
                ('student_id', models.CharField(max_length=100)),
            ],
        ),
    ]
