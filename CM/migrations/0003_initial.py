# Generated by Django 4.2.6 on 2024-04-09 10:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('CM', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessons',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='seat',
            unique_together={('classroom', 'row', 'column')},
        ),
    ]
