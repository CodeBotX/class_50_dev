# Generated by Django 4.2.6 on 2024-03-28 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CM', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessons',
            name='grade',
            field=models.IntegerField(choices=[('10', 'Tốt'), ('8', 'Khá'), ('6', 'Trung Bình'), ('4', 'Yếu')], default='10'),
        ),
    ]
