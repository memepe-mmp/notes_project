from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Category, Note, Tag

class IndexQueriesTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create(username="u")
        cat = Category.objects.create(name="c")
        tag = Tag.objects.create(name="t")
        for i in range(60):
            note = Note.objects.create(title=f"n{i}", owner=user, category=cat)
            note.tags.add(tag)

    def test_query_count_does_not_grow(self):
        with self.assertNumQueries(4):
            self.client.get("/")
