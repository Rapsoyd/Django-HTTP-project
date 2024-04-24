"""
Каталог утилит
"""
from uuid import uuid4
from pytils.translit import slugify


def unique_slugify(instance, model_title):
    """
    Генератор уникального слага
    """
    model = instance.__class__  # Получаем модель
    unique_slug = slugify(model_title)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{unique_slug}-{uuid4().hex[:4]}"
    return unique_slug
        