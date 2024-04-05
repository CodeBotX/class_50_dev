# Generated by Django 4.2.6 on 2024-04-05 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lessons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('counter', models.PositiveIntegerField(default=1)),
                ('comment', models.TextField()),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('grade', models.IntegerField(choices=[(10, 'Tốt'), (8, 'Khá'), (6, 'Trung Bình'), (4, 'Yếu')], default='10')),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.PositiveIntegerField()),
                ('column', models.PositiveIntegerField()),
            ],
        ),
    ]
