# Generated by Django 5.1.4 on 2024-12-31 09:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, verbose_name="Название курса"),
                ),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="materials/courses/previews",
                        verbose_name="Превью курса",
                    ),
                ),
                ("description", models.TextField(verbose_name="Описание курса")),
            ],
            options={
                "verbose_name": "Курс",
                "verbose_name_plural": "Курсы",
            },
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, verbose_name="Название урока"),
                ),
                ("description", models.TextField(verbose_name="Описание урока")),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="materials/lessons/previews",
                        verbose_name="Превью урока",
                    ),
                ),
                ("video_url", models.URLField(verbose_name="Ссылка на видео")),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lessons",
                        to="materials.course",
                        verbose_name="Курс",
                    ),
                ),
            ],
            options={
                "verbose_name": "Урок",
                "verbose_name_plural": "Уроки",
            },
        ),
    ]
