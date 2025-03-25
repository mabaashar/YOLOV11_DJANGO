# Generated by Django 5.0.3 on 2025-01-11 10:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('threshold', '0031_alter_threshold_component_model1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='threshold_component',
            name='model1',
            field=models.ForeignKey(default='YOLO11 Defaul detection Model', on_delete=django.db.models.deletion.CASCADE, related_name='ip_cam_1_model', to='threshold.yolo_model'),
        ),
        migrations.AlterField(
            model_name='threshold_component',
            name='model2',
            field=models.ForeignKey(default='YOLO11 Defaul detection Model', on_delete=django.db.models.deletion.CASCADE, related_name='ip_cam_2_model', to='threshold.yolo_model'),
        ),
        migrations.AlterField(
            model_name='threshold_component',
            name='model3',
            field=models.ForeignKey(default='YOLO11 Defaul detection Model', on_delete=django.db.models.deletion.CASCADE, related_name='ip_cam_3_model', to='threshold.yolo_model'),
        ),
        migrations.AlterField(
            model_name='threshold_component',
            name='model4',
            field=models.ForeignKey(default='YOLO11 Defaul detection Model', on_delete=django.db.models.deletion.CASCADE, related_name='ip_cam_4_model', to='threshold.yolo_model'),
        ),
        migrations.AlterField(
            model_name='threshold_component',
            name='model5',
            field=models.ForeignKey(default='YOLO11 Defaul detection Model', on_delete=django.db.models.deletion.CASCADE, related_name='ip_cam_5_model', to='threshold.yolo_model'),
        ),
    ]
