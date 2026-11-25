from django.core.cache import cache
from django.db.models import Count
import logging
import time

from .models import Category

CATEGORIES_KEY = "categories_with_counts"

def get_categories_with_counts():
    return cache.get_or_set(
        CATEGORIES_KEY,
        lambda:
list(Category.objects.annotate(notes_count=Count("notes")).order_by("name")),
        timeout=600,
    )

logger = logging.getLogger(__name__)

def notify_external_service(note):
    time.sleep(3)
    logger.warning("Внешний сервис уведомлён о заметке %s", note.pk)