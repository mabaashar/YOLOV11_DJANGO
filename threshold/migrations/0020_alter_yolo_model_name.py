# Generated by Django 5.0.3 on 2025-01-10 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('threshold', '0019_alter_yolo_model_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yolo_model',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
