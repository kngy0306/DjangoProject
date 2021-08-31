from django.urls import path
from . import views

# URLパターンを逆引きできるように名前をつける
app_name = 'photo'

# URLパターンを登録するための変数
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post/', views.CreatePhotoView.as_view(), name='post'),
    path('post_done/', views.PostSuccessView.as_view(), name='post_done'),
    path('photos/<int:category>', views.CategoryView.as_view(), name='photos_cat'),
    path('user_list/<int:user>', views.UserView.as_view(), name='user_list'),
]
