from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from django.http import Http404, JsonResponse
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.db import transaction # トランザクション
from django.views.decorators.http import require_POST # api_like
from .forms import SignUpForm
from app.models import Article, Comment

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # ユーザー登録後にリダイレクトするページ
        else:
            print("フォームエラー", form.errors) # バリエーションエラーがあればエラーメッセージを出力（テスト用）
    else:
        form = SignUpForm()
    return render(request, 'app/signup.html', {'form': form})

def home(request):
    # ソート処理
    sort = request.GET.get('sort')
    if sort == 'asc':
        articles = Article.objects.order_by('posted_at')
    elif sort == 'desc':
        articles = Article.objects.order_by('-posted_at')
    else:
        # 無効なパラメータが指定された場合のデフォルト動作
        articles = Article.objects.order_by('-posted_at')  # デフォルトで降順に設定

    # ページネーション処理
    paginator = Paginator(articles, 5)  # 1ページに5件の記事を表示
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    
    return render(request, 'app/home.html', context)

def public_page(request):
    return render(request, 'app/public.html', {})

@login_required
def create_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('text')

        if not title or not body:
            return HttpResponse("タイトルと本文は必須です。", status=400)

        try:
            article = Article.objects.create(
                title=title,
                body=body,
                author=request.user
            )
            return redirect('home')  # 投稿成功時には一覧ページにリダイレクト
        except Exception as e:
            return HttpResponse("記事の保存中にエラーが発生しました: " + str(e), status=500)

    return render(request, 'app/create.html', {})

'''トランザクション実装バージョン
@login_required
def create_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('text')

        if not title or not body:
            return HttpResponse("タイトルと本文は必須です。", status=400)

        try:
            with transaction.atomic():
                article = Article(
                    title=title,
                    body=body,
                    author=request.user
                )
                article.save()
            return redirect('home')  # 投稿成功時には一覧ページにリダイレクト
        except Exception as e:
            return HttpResponse("記事の保存中にエラーが発生しました: " + str(e), status=500)

    # POSTでない場合はフォームページを表示
    return render(request, 'app/create.html', {})
'''

def like(request, article_id):
    try:
        with transaction.atomic():
            article = Article.objects.select_for_update().get(pk=article_id)
            article.like += 1
            article.save()
    except Article.DoesNotExist:
        raise Http404("Article does not exist")

    return redirect(detail, article_id)
'''トランザクション実装前
def like(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
        article.like += 1
        article.save()

    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    
    return redirect(detail, article_id)    
'''

def api_like(request, article_id):
    try:
        with transaction.atomic():
            article = Article.objects.select_for_update().get(pk=article_id)
            article.like += 1
            article.save()
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    
    result = {
        'id': article_id,
        'like': article.like,
    }
    return JsonResponse(result)
'''トランザクション実装前
def api_like(request, article_id): #api
    try:
        article = Article.objects.get(pk=article_id)
        article.like += 1
        article.save()
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    result = {
        'id': article_id,
        'like': article.like,
    }
    return JsonResponse(result)    
'''
#@login_required
def detail(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")

    if request.method == 'POST':
        try:
            Comment.objects.create(article=article, text=request.POST['text'], author=request.user)
        except Exception as e:
            return HttpResponse("コメントの保存中にエラーが発生しました: " + str(e), status=500)

    context = {
        'article': article,
        'comments': article.comments.order_by('-posted_at'),
    }
    return render(request, "app/detail.html", context)

'''トランザクション制御バージョン
def detail(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")

    if request.method == 'POST':
        try:
            with transaction.atomic():
                comment = Comment(article=article, text=request.POST['text'], author=request.user)
                comment.save()
        except Exception as e:
            return HttpResponse("コメントの保存中にエラーが発生しました: " + str(e), status=500)

    context = {
        'article': article,
        'comments': article.comments.order_by('-posted_at'),
    }
    return render(request, "app/detail.html", context)
'''
@login_required
def update(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    
    if request.method == 'POST':
        try:
            article.title = request.POST['title']
            article.body = request.POST['text']
            article.save()
            return redirect(detail, article_id)
        except Exception as e:
            return HttpResponse("記事の更新中にエラーが発生しました: " + str(e), status=500)
    
    context = {'article': article}
    return render(request, "app/edit.html", context)
'''トランザクション制御バージョン
@login_required
def update(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                article.title = request.POST['title']
                article.body = request.POST['text']
                article.save()
            return redirect(detail, article_id)
        except Exception as e:
            return HttpResponse("記事の更新中にエラーが発生しました: " + str(e), status=500)
    
    context = {'article': article}
    return render(request, "app/edit.html", context)
'''
'''トランザクション実装前
@login_required
def update(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    if request.method == 'POST':
        article.title = request.POST['title']
        article.body = request.POST['text']
        article.save()
        return redirect(detail, article_id)
    context = {
        'article': article
    }    
    return render(request, "app/edit.html", context)
'''
@login_required
def delete(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    
    if request.method == 'POST':
        try:
            article.delete()
            return redirect(home)
        except Exception as e:
            return HttpResponse("記事の削除中にエラーが発生しました: " + str(e), status=500)
    
    return redirect(home)
'''トランザクション制御バージョン
@login_required
def delete(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                article.delete()
            return redirect(home)
        except Exception as e:
            return HttpResponse("記事の削除中にエラーが発生しました: " + str(e), status=500)
    
    return redirect(home)
'''    
'''
@login_required
def private_page(request):
    return render(request, 'app/private.html', {})
'''

