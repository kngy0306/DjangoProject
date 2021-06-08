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
python manage.py startapp tutorial
```  

#### ビューの作成
`tutorial/views.py`  
```python
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('<h1>Hello, Kona</h1>')
```

ビューを呼ぶためにURLを対応付けする。→ <b>URLconf</b>が必要。

tutorialディレクトリにURLconfを作成するため、`urls.py`を作成する。  

```python
from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name='index'),
]
```

続いて、ルートの<b>URLconf</b>にtutorial.urlsモジュールの記述を反映させる。

`djangoApp/urls.py`にimportを追加する。
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('tutorial/', include('tutorial.urls')),
    path('admin/', admin.site.urls),
]
```

`include()`関数で他の`URLconf`を参照することができる。

## はじめての Django アプリ作成、その 2
### DBの設定
djangoApp/setting.py
```python
TIME_ZONE = 'JP'
```

migrateコマンドでsetting.py内のINSTALLED_APPを参照し、setting.pyファイルのDB設定に従って必要なDBのテーブルを作成する。  
`python manage.py migrate`  

### モデルの作成
tutorial/models.py
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
