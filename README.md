## Django_Tutorial

### 公式チュートリアル
https://docs.djangoproject.com/ja/3.2/intro/tutorial01/

### Dockerを使用したDjangoプロジェクト作成 参考サイト
https://qiita.com/homines22/items/2730d26e932554b6fb58


### migrate
```python3 manage.py makemigrations```  
```python3 manage.py migrate```


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
KONA
12345678

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
```python
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
```

polls/urls.py
```python
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
```python
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
```python
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
```python
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

## はじめての Django アプリ作成、その 3
### フォームを書く
forloop.counter でforタグが何回実行されたか表せる。  
CSRFは{% csrf_token %}を記述することで対策できる。
```python
<form action="{% url 'polls:vote' question.id %}" method="post">
  {% csrf_token %}
  <fieldset>
    <legend>
      <h1>{{ question.question_text }}</h1>
    </legend>
    {% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}
    {% for choice in question.choice_set.all %}
    <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
    <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
    {% endfor %}
  </fieldset>
</form>
```

### ↑のフォームを受け取る関数
pk=request.POST['choice']は辞書のようなオブジェクト。キー指定でinputのnameを受け取れる？常に文字列  
POSTデータにchoiceがない場合、request.POST['choice']はKeyErrorを出す。その場合exceptでキャッチしてエラー文とともに再度フォームに返す。  
reverse関数でurls.py内のnameで指定しているものを使える。
```python
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # フォームを再度繰り返す
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'You didnt select a choice.',
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # ユーザーがフォームに戻り２回目の投票を防ぐためにHttpResponseRedirectを返す
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
```

### 汎用ビューを使用する
1. URLconfを変換する
1. 古いビューを削除する
1. 汎用ビューにする

ListViewとDetailView の使用。それぞれ「オブジェクトのリストを表示する」「あるタイプのオブジェクトの詳細ページを表示する」という概念を抽象化している。

```python
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    ... # same as above, no changes needed.
```

### 2021-0613 挫折