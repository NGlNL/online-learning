from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название курса')
    preview = models.ImageField(upload_to='materials/courses/previews', verbose_name='Превью курса', blank=True, null=True)
    description = models.TextField(verbose_name='Описание курса', blank=True)
    objects = models.Manager()

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')
    name = models.CharField(max_length=100, verbose_name='Название урока')
    description = models.TextField(verbose_name='Описание урока', blank=True)
    preview = models.ImageField(upload_to='materials/lessons/previews', verbose_name='Превью урока', blank=True, null=True)
    video_url = models.URLField(verbose_name='Ссылка на видео', blank=True)
    objects = models.Manager()

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.name
