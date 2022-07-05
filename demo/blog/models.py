from django.db import models
from django.db.models.fields import DateTimeField
from django.utils import timezone
from django.contrib.auth.models import User





class Category(models.Model):
    title = models.CharField('Загаловок', max_length=250)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


    def __str__(self):
        return self.title


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', null=True)
    title = models.CharField('Загаловок', max_length=250)
    body = models.TextField('Контенет')
    image = models.FileField('Фото', blank=True)
    date = models.DateTimeField('Дата', default=timezone.now())
    

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


    def __str__(self):
        return self.title



class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Ползователь')
    date = models.DateField('Дата рождения', blank=True, null=True)

    class Meta:
        verbose_name = 'Юзер'
        verbose_name_plural = 'Юзеры'


    def __str__(self):
        return self.user.username




class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='User')
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE, related_name='post_comments', verbose_name='Пост')
    text = models.TextField('Коммент')
    date = DateTimeField('Дата добавления', default=timezone.now())


    class Meta:
        verbose_name = 'Коммент'
        verbose_name_plural = 'Комменты'


    def __str__(self):
        return self.user.username



class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_favourites', verbose_name='User')
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE, related_name='post_favourites', verbose_name='Пост')


    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


    def __str__(self):
        return self.user.username + "|" + self.post.title


class Like(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_likes', verbose_name='User')
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE, related_name='post_likes', verbose_name='Пост')


    class Meta:
        verbose_name = 'Лайки'
        verbose_name_plural = 'Лайки'


    def __str__(self):
        return self.post.title


class Dislike(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_dislikes', verbose_name='User')
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE, related_name='post_dislikes', verbose_name='Пост')


    class Meta:
        verbose_name = 'Дизлайки'
        verbose_name_plural = 'Дизлайки'


    def __str__(self):
        return self.post.title