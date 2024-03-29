from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from utils.slug import unique_slugify

User = get_user_model()


class Article(models.Model):
    """
    Модель постов для блога
    """

    class ArticleManager(models.Manager):
        """
        Кастомный менеджер для модели статей
        """

        def all(self):
            """
            Получает все опубликованные статьи
            """
            return self.get_queryset().select_related("author", "category").filter(status="published")

    STATUS_OPTIONS = (("published", "Опубликовано"), ("draft", "Черновик"))

    title = models.CharField(verbose_name="Заголовок", max_length=255)
    slug = models.SlugField(verbose_name="URL", max_length=255, blank=True, unique=True)
    short_description = models.TextField(verbose_name="Краткое описание", max_length=500)
    full_description = models.TextField(verbose_name="Полное описание")
    thumbnail = models.ImageField(
        verbose_name="Превью поста",
        blank=True,
        upload_to="images/thumbnails/%Y/%m/%d/",
        validators=[FileExtensionValidator(allowed_extensions=("png", "jpg", "webp", "jpeg", "gif"))],
    )
    status = models.CharField(choices=STATUS_OPTIONS, default="draft", verbose_name="Статус поста", max_length=20)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    author = models.ForeignKey(
        to=User, verbose_name="Автор", on_delete=models.SET_DEFAULT, related_name="author_posts", default=1
    )
    anchored = models.BooleanField(verbose_name="Закреплено", default=False)
    category = TreeForeignKey("Category", on_delete=models.PROTECT, related_name="articles", verbose_name="Категория")

    objects = ArticleManager()

    class Meta:
        db_table = "app_articles"
        ordering = ["-anchored", "-created_at"]
        indexes = [models.Index(fields=["-anchored", "-created_at", "status"])]
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)


class Category(MPTTModel):
    """
    Модель категорий с вложенностью
    """

    title = models.CharField(max_length=255, verbose_name="Название категории")
    slug = models.SlugField(max_length=255, verbose_name="URL категории", blank=True)
    description = models.TextField(verbose_name="Описание категории", max_length=300)
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name="children",
        verbose_name="Родительская категория",
    )

    class MPTTMeta:
        order_insertion_by = ("title",)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        db_table = "app_categories"

    def __str__(self):
        return self.title
