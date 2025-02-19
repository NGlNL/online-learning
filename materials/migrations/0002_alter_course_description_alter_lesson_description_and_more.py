# Generated by Django 5.1.4 on 2025-01-12 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="description",
            field=models.TextField(blank=True, verbose_name="Описание курса"),
        ),
        migrations.AlterField(
            model_name="lesson",
            name="description",
            field=models.TextField(blank=True, verbose_name="Описание урока"),
        ),
        migrations.AlterField(
            model_name="lesson",
            name="video_url",
            field=models.URLField(blank=True, verbose_name="Ссылка на видео"),
        ),
    ]
