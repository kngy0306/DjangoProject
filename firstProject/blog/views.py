from django.shortcuts import render

# django.views.generic.baseからTemplateViewをインポートする
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    # クラスベースのview
    # 関数ベースの際に必要な処理をブラックボックス化してくれている
    template_name = "index.html"
