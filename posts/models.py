from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Post(models.Model):
    text = models.TextField('Текст статьи', help_text='Что у вас нового?')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор статьи')
    group = models.ForeignKey('Group', blank=True, null=True, on_delete=models.SET_NULL,
                              verbose_name='Тематика статьи', help_text='Можете выбрать тематику')
    image = models.ImageField('Изображение', upload_to='posts/', blank=True, null=True,
                              help_text='Можете загрузить изображение')

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.text[:30]


class Group(models.Model):
    title = models.CharField('Название тематики', max_length=200, null=False)
    slug = models.SlugField('Url адрес тематики', unique=True)
    description = models.TextField('Описание тематики')

    class Meta:
        verbose_name = 'Тематика'
        verbose_name_plural = 'Тематики'

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE,
                             verbose_name='Cтатья с комментариями')
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE,
                               verbose_name='Автор комментария')
    text = models.TextField('Комментарий', help_text='Напишите комментарий')
    created = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-created']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Follow(models.Model):
    user = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE, verbose_name='Подписчик')
    author = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE, verbose_name='Отслеживается')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('user', 'author')
