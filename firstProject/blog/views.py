from django.shortcuts import render

# django.views.genericからListViewをインポートする
from django.views.generic import ListView, DetailView

from .models import BlogPost


class IndexView(ListView):
    '''トップページビュー

    投稿記事を一覧表示するのでListViewを継承する

    Attributes:
        template_name: レンダリングするテンプレート
        context_object_name: object_listキーの別名を設定
        queryset: DBのクエリ
    '''

    template_name = "index.html"
    # object_listキーの別名を設定
    context_object_name = "orderby_records"
    # BlogPostレコードを、投稿日時の降順で表示
    queryset = BlogPost.objects.order_by("-posted_at")

    paginate_by = 4


class BlogDetail(DetailView):
    '''詳細ページのビュー

    投稿記事の詳細を表示するのでDetailViewを継承する

    Attributes:
        template_name: レンダリングするテンプレート
        Model: モデルのクラス
    '''
    template_name = "post.html"
    model = BlogPost


class NogizakaView(ListView):
    template_name = "nogizaka.html"
    model = BlogPost
    context_object_name = "nogizaka_records"
    queryset = BlogPost.objects.filter(
        category="nogizaka").order_by("-posted_at")
    paginate_by = 2


class HinatazakaView(ListView):
    template_name = "hinatazaka.html"
    model = BlogPost
    context_object_name = "hinatazaka_records"
    queryset = BlogPost.objects.filter(
        category="hinatazaka").order_by("-posted_at")
    paginate_by = 2


class SakurazakaView(ListView):
    template_name = "sakurazaka.html"
    model = BlogPost
    context_object_name = "sakurazaka_records"
    queryset = BlogPost.objects.filter(
        category="sakurazaka").order_by("-posted_at")
    paginate_by = 2
