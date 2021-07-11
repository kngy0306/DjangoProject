from django.db import models


class BlogPost(models.Model):
    '''モデルクラス'''
    CATEGORY = (("nogizaka", "乃木坂46"),
                ("hinatazaka", "日向坂46"), ("sakurazaka", "櫻坂46"))

    # タイトル用フィールド
    title = models.CharField(
        verbose_name="タイトル",
        max_length=200,
    )

    # 本文用タイトル
    content = models.TextField(
        verbose_name="本文",
    )

    # 投稿日時のフィールド
    posted_at = models.DateTimeField(
        verbose_name="投稿日時",
        auto_now_add=True,
    )

    # カテゴリのフィールド
    category = models.CharField(
        verbose_name="カテゴリ",
        max_length=50,
        choices=CATEGORY,
    )

    def __str__(self):
        return self.title
