from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Article
#from app.models import Article

class ArticleIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        logged_in = self.client.login(username="testuser", password="password")
        self.assertTrue(logged_in, "ログインに失敗しました")

    def test_create_and_view_article(self):
        url = reverse('create')
        response = self.client.post(url, {
            'title': 'New Article',
            'text': 'Content of the new article.'
        })
        self.assertEqual(response.status_code, 302)  # リダイレクトが発生することを期待
        # リダイレクト後に記事が存在することを確認
        self.assertTrue(Article.objects.filter(title="New Article").exists())
'''
    def test_create_and_view_article(self):
        # 記事を作成する
        response = self.client.post(reverse('create'), {
            'title': 'Integration Test Article',
            'body': 'This is a test article for integration test.',
        })
        # 作成された後のリダイレクト確認
        self.assertEqual(response.status_code, 302)

        # 投稿された記事を取得して詳細表示を確認
        article = Article.objects.get(title="Integration Test Article")
        response = self.client.get(reverse('detail', args=[article.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Integration Test Article")
'''
class ArticleLikeTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.article = Article.objects.create(
            title="Like Test Article", 
            body="This article is for like testing.", 
            author=self.user
        )

    def test_like_article(self):
        # 「いいね」を追加
        response = self.client.post(reverse('like', args=[self.article.id]))
        # データベースから最新の状態を取得
        self.article.refresh_from_db()
        self.assertEqual(self.article.like, 1)