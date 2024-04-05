# Generated by Django 4.2.7 on 2024-04-05 17:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('SM', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classroom', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='schedule',
            unique_together={('classroom', 'dayofweek', 'period')},
        ),
    ]
