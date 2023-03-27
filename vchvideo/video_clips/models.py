from django.db import models
from django.urls import reverse

from .utilities import get_timestamp_path


# модель публикации
class Video(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name='Выводить в списке?')
    price = models.TextField(verbose_name='Цена')
    url = models.URLField(verbose_name='Ссылка на видео')
    created_dt = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата, время')
    categ = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')

    # удалит всю запись и дополнительные иллюстрации
    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, *kwargs)

    # при просмотре данных таблицы в терминале, выводить загаловки записей
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name_plural = 'Все публикации'
        verbose_name = 'Публикация'
        # ordering = ['-created_dt']
        ordering = ['-id']


# доп иллюстрации
class AdditionalImage(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name='Публикация')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name="Доп изображения")

    class Meta:
        verbose_name_plural = 'Дополнительные иллюстрации'
        verbose_name = 'Дополнительная иллюстрация'


class Category(models.Model):
    name = models.CharField(max_length=40, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name_plural = 'Все категории'
        verbose_name = 'Категория'
        ordering = ['id']