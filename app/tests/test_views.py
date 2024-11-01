from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Article
#from app.models import Article

class ArticleListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")  # ログイン状態にする

    def test_article_list_view_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_article_list_pagination(self):
        response = self.client.get(reverse('home'))
        self.assertTrue('page_obj' in response.context)
        self.assertTrue(response.context['page_obj'].paginator.num_pages >= 1)

class ArticleDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.article = Article.objects.create(title="Test Article", body="Detailed test", author=self.user)

    def test_article_detail_view(self):
        response = self.client.get(reverse('detail', args=[self.article.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Article")

class ArticleCreateViewTest(TestCase):
    def setUp(self):
        # テストユーザーの作成とログイン
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_article_create_view(self):#変更したところ
        # 記事作成ページのURLを取得
        url = reverse('home')  # 'home'は作成ページのURL名

        # POSTリクエストでデータを送信し、記事作成を試みる
        response = self.client.post(url, {
            'title': 'New Article',
            'text': 'Content of the new article.',
        })

        # デバッグ用にフォームのエラーメッセージを表示
        if response.context and 'form' in response.context:
            print("Form errors:", response.context['form'].errors)
        else:
            print("No form in context or context is None - status:", response.status_code)
            print("Response content:", response.content)

        # 記事が作成されたか確認
        self.assertTrue(Article.objects.filter(title="New Article").exists())
        