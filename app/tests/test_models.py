from django.test import TestCase
from django.contrib.auth.models import User
#from ..models import Article
from app.models import Article
from django.utils import timezone

class ArticleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.article = Article.objects.create(
            title="Test Article",
            body="This is a test article.",
            author=self.user,
            posted_at=timezone.now()
        )

    def test_article_str_method(self):
        self.assertEqual(str(self.article), "Test Article")

    def test_article_publish_method(self):
        self.article.publish()
        self.assertIsNotNone(self.article.published_at)