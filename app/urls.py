from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # ログアウトURL
    #path('priv', views.private_page, name='priv'),
    path('pub/', views.public_page, name='pub'),
    path('create/', views.create_page, name='create'), # 名前が統一されていない
    path('<int:article_id>/', views.detail, name='detail'),
    path('<int:article_id>/delete/', views.delete, name='delete'),
    path('<int:article_id>/update/', views.update, name='update'),
    path('<int:article_id>/like/',views.like, name='like'),
    path('api/articles/<int:article_id>/like/', views.api_like),
]