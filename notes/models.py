from django.conf import settings
from django.db import models
from django.db.models import Q
from django.contrib.postgres.indexes import GinIndex, OpClass
from django.db.models.functions import Upper

class Category(models.Model):
    name = models.CharField("Название", max_length=100, unique=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField("Название", max_length=50, unique=True)

    def __str__(self):
        return self.name

class Note(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    text = models.CharField("Текст", blank=True)
    is_done = models.BooleanField("Выполнено", default=False)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Изменено", auto_now=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True, related_name="notes", verbose_name="Автор",
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="notes", verbose_name="Категория",
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="notes",
verbose_name="Теги")

    class Meta:
        ordering = ["-created_at", "-id"]
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"
        indexes = [
            models.Index(fields=["-created_at", "-id"], name="note_created_idx"),
            models.Index(fields=["category", "-created_at", "-id"],
    name="note_cat_created_idx"),
            models.Index(
                fields=["-created_at", "-id"],
                condition=Q(is_done=False),
                name="note_active_created_idx",
            ),
            GinIndex(OpClass(Upper("title"), name="gin_trgm_ops"), name="note_title_trgm_idx"),
        ]

    def __str__(self):
        return self.title
