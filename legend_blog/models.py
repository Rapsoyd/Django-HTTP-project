from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from services.utils import unique_slugify
from django.urls import reverse
from django.core.validators import MinLengthValidator


class Post(models.Model):
    """
    Модель для постов блога
    """

    STATUS_OPTIONS = (("published", "Опубликовано"), ("draft", "Черновик"))
    author = models.ForeignKey(
        to=User,
        verbose_name="Автор записи",
        on_delete=models.CASCADE,
        related_name="author_posts",
    )
    title = models.CharField(verbose_name="Название записи", max_length=80)
    slug = models.SlugField(verbose_name="URL", max_length=120, blank=True)
    text = models.TextField(verbose_name="Текст записи",
                            validators=[MinLengthValidator(31)],
                            max_length=950)
    thumbnail = models.ImageField(
        default="blog/default.jpg",
        verbose_name="Изображение записи",
        blank=True,
        upload_to="images/thumbnail/%Y/%m/%d",
        validators=[
            FileExtensionValidator(allowed_extensions=("png", "jpg", "jpeg",
                                                       "webp", "gif"))
        ],
    )
    status = models.CharField(
        choices=STATUS_OPTIONS,
        default="published",
        verbose_name="Статусы записей",
        max_length=13,
    )
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name="Время добавления")
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name="Время обновления")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "blog_post"
        ordering = ["-created"]
        indexes = [models.Index(fields=["-created", "-status"])]
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)


class PostReaction(models.Model):
    RATE_OPTIONS = (("clown", "Клоун"), ("like", "Круть"), ("dislike", "Ужас"))
    user = models.ForeignKey(to=User,
                             verbose_name="Пользователь",
                             on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post,
                             verbose_name="Пост",
                             on_delete=models.CASCADE)
    reaction = models.CharField(max_length=10,
                                verbose_name="Тип реакции",
                                choices=RATE_OPTIONS)

    class Meta:
        indexes = [models.Index(fields=['reaction'])]
        unique_together = ("user", "post")
        verbose_name = "Реакция на пост"
        verbose_name_plural = "Реакции на посты"
        db_table = "reaction"


class PostComment(models.Model):
    post = models.ForeignKey(to=Post,
                             on_delete=models.CASCADE,
                             related_name="comments")
    nickname = models.CharField(max_length=20)
    email = models.EmailField()
    body = models.TextField(max_length=450)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created"]
        indexes = [models.Index(fields=["created"])]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"Comment by {self.nickname} on {self.post}"
