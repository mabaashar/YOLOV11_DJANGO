# Generated by Django 5.0.3 on 2025-01-10 09:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('threshold', '0016_yolo_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='threshold_component',
            name='model1',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ip_cam_1_model', to='threshold.yolo_model'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='threshold_component',
            name='model2',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ip_cam_2_model', to='threshold.yolo_model'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='threshold_component',
            name='model3',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ip_cam_3_model', to='threshold.yolo_model'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='threshold_component',
            name='model4',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ip_cam_4_model', to='threshold.yolo_model'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='threshold_component',
            name='model5',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ip_cam_5_model', to='threshold.yolo_model'),
            preserve_default=False,
        ),
    ]
