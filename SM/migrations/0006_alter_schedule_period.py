# Generated by Django 4.2.6 on 2024-03-28 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SM', '0005_alter_schedule_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SM.lessontime'),
        ),
    ]
