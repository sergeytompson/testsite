from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    content = models.TextField(blank=True, verbose_name='Текст Новости')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано в')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Отредактировано в')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    is_publish = models.BooleanField(default=True, verbose_name='Опубликовано')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name='Категория')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Comments(models.Model):
    username = models.CharField(max_length=100, verbose_name='Имя пользователя')
    text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано в')
    news = models.ForeignKey(News, on_delete=models.PROTECT, verbose_name='Новость')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('news', kwargs={'pk': self.news})
