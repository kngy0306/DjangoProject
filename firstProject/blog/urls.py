from django.urls import path
from . import views

app_name = 'blog'

# viewsモジュールのIndexViewクラスをインスタンス化する
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('blog-detail/<int:pk>/', views.BlogDetail.as_view(), name="blog_detail"),
    path('nogizaka-list/', views.NogizakaView.as_view(), name="nogizaka_list"),
    path('hinatazaka-list/', views.HinatazakaView.as_view(), name="hinatazaka_list"),
    path('sakurazaka-list/', views.SakurazakaView.as_view(), name="sakurazaka_list"),
]
