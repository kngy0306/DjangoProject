from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # http(s)://<ホスト名>/ 以下に当てはまるパスにマッチングした場合
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]
