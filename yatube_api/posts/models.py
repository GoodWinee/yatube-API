from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import Truncator

from posts.constants import MAX_LENGTH_TEXT

User = get_user_model()


class Group(models.Model):
    """Модель сообщества."""

    title = models.CharField(
        'Сообщество',
        max_length=200
    )
    slug = models.SlugField(
        'Страница сообщества',
        max_length=50
    )
    description = models.TextField(
        'Описание'
    )

    class Meta:
        default_related_name = 'groups'

    def __str__(self):
        return self.title


class Post(models.Model):
    """Модель поста."""

    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    image = models.ImageField(
        upload_to='posts/',
        null=True,
        blank=True
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Сообщество'
    )

    class Meta:
        ordering = (
            'pub_date',
        )
        default_related_name = 'posts'

    def __str__(self):
        truncated_text = Truncator(self.text).chars(MAX_LENGTH_TEXT)
        return f'Пост от {self.author}: {truncated_text}'


class Comment(models.Model):
    """Модель комментария."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        default_related_name = 'comments'

    def __str__(self):
        truncated_comment = Truncator(self.text).chars(MAX_LENGTH_TEXT)
        truncated_post = Truncator(str(self.post)).chars(MAX_LENGTH_TEXT)
        return (f'Комментарий от {self.author.username} '
                f'к посту "{truncated_post}" '
                f': "{truncated_comment}" '
                )


class Follow(models.Model):
    """Модель подписки."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follows',
        verbose_name='Подписаться'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user.username} подписан на {self.following.username}'
