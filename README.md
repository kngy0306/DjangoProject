## Django_Tutorial

### 公式チュートリアル
https://docs.djangoproject.com/ja/3.2/intro/tutorial01/

### Dockerを使用したDjangoプロジェクト作成 参考サイト
https://qiita.com/homines22/items/2730d26e932554b6fb58


## はじめての Django アプリ作成、その 1
#### プロジェクトの作成
最初にセットアップを行う。Djangoのプロジェクトを構成するコードを自動生成。  
プロジェクト ... DBの設定やDjango固有のオプションの設定などのDjangoインスタンスの設定を集めたもの。  

```bash
django-admin startproject djangoApp
```  

#### アプリケーションの作成
Djangoには基本的なディレクトリ構造を自走で生成してくれるので、コードを書くことに専念できる。  

`manage.py`と同じディレクトリで、  
```bash
python manage.py startapp polls
```  

#### ビューの作成
`polls/views.py`  
```python
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('<h1>polls/</h1>')
```

ビューを呼ぶためにURLを対応付けする。→ <b>URLconf</b>が必要。

pollsディレクトリにURLconfを作成するため、`urls.py`を作成する。  

```python
from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name='index'),
]
```

続いて、ルートの<b>URLconf</b>にpolls.urlsモジュールの記述を反映させる。

`djangoApp/urls.py`にimportを追加する。
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
```

`include()`関数で他の`URLconf`を参照することができる。

## はじめての Django アプリ作成、その 2
### DBの設定
djangoApp/setting.py
```python
TIME_ZONE = 'Asia/Tokyo'
```

migrateコマンドでsetting.py内のINSTALLED_APPを参照し、setting.pyファイルのDB設定に従って必要なDBのテーブルを作成する。  
`python manage.py migrate`  

### モデルの作成
polls/models.py
```python
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```

いずれもdjango.db.models.Modelのサブクラス。  
マイグレーションはDjangoがモデルの変更を保存する方法。  
`migrate`を実行し、モデルのテーブルをDBに作成する。  
```
python3 manage.py migrate
```

モデルの変更を実施するためには
- モデルを変更する（models.py）。
- これらの変更のためのマイグレーションを作成するために python3 manage.py makemigrations を実行する。
- ータベースにこれらの変更を適用するために python manage.py migrate を実行する。

### 管理ユーザの作成
adminサイトにログインできるユーザの作成。
```
python3 manage.py createsuperuser
```

http://127.0.0.1:8000/admin/ にアクセス。

adminページでアプリを操作するために、`Question`オブジェクトがadminインターフェースを持つということをadminに教える  
polls/admin.py
```
from django.contrib import admin

from .models import Question

admin.site.register(Question)
```

## はじめての Django アプリ作成、その 3
### ビュー
Djangoのアプリケーションにおいて特定の機能を提供するウェブページの<b>型</b>であり、各々のテンプレートを保持している。
- Blog ホームページ - 最新エントリーをいくつか表示
- エントリー詳細ページ - 1エントリーへのパーマリンク (permalink) ページ
- 年ごとのアーカイブページ - 指定された年のエントリーの月を全て表示
- 月ごとのアーカイブページ - 指定された月のエントリーの日をすべて表示
- 日ごとのアーカイブページ - 指定された日の全てのエントリーを表示
- コメント投稿 - エントリーに対するコメントの投稿を受付
投票アプリケーションでは、以下4つのビューを作成します:
- 質問 "インデックス" ページ -- 最新の質問をいくつか表示
- 質問 "詳細" ページ -- 結果を表示せず、質問テキストと投票フォームを表示
- 質問 "結果" ページ -- 特定の質問の結果を表示
- 投票ページ -- 特定の質問の選択を投票として受付

URLからビューを得るためにDjangoは<b>URLconf</b>を使用する。URLパターンをビューにマッピングする。  
polls/views.py
```
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
```

polls/urls.py
```
from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
```

### テンプレートを使う
polls/templates/polls/index.html
異なるアプリケーション内に同じ名前のテンプレートがあった場合に区別できないため、templatesの中に名前空間としてpollsディレクトリを作成している。
```
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}
```
polls/views.py
```
from django.http import HttpResponse
from django.template import loader

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
```

### URL名の名前空間
現段階ではpollsアプリ1つだけだが、複数持つとき、{% url 'detail' %}などとした場合、他のアプリのdetailと被ることを防ぐためにpolls/urls.pyにapp_nameを追加する。  
変更後は{% url 'polls:detail' %}となる。
```
from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
```

