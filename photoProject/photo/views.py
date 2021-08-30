from django.shortcuts import render
# TemplateView, CreateViewをインポート
from django.views.generic import TemplateView, CreateView, ListView
# reverse_lazyをインポート
from django.urls import reverse_lazy
# PhotoPostFormをインポート
from .forms import PhotoPostForm
# method_decoratorをインポート
from django.utils.decorators import method_decorator
# login_requiredをインポート
from django.contrib.auth.decorators import login_required
# modelsモジュールからモデルPhotoPostをインポート
from .models import PhotoPost


class IndexView(ListView):
    '''トップページのビュー
    '''
    template_name = 'index.html'
    # モデルPhotoPostのオブジェクトにorder_by()を適応して投稿日時の降順で並び替え
    queryset = PhotoPost.objects.order_by('-posted_at')
    # 1ページに表示するレコード件数
    paginate_by = 6

# デコレータによりCreatePhotoViewへのアクセスはログインユーザーに限定される
# ログイン状態でなければsettings.pyのLOGIN_URLにリダイレクト


@method_decorator(login_required, name='dispatch')
class CreatePhotoView(CreateView):
    '''写真投稿ページのビュー

    PhotoPostFormで定義されているモデルとフィールドと連携して投稿データをDBに登録する

    Attributes:
        form_class: モデルとフィールドが登録されたフォームクラス
        template_name: レンダリングするテンプレート
        success_url: DBへの登録完了後、リダイレクト先
    '''
    # forms.pyのPhotoPostFormをフォームクラスとして登録
    form_class = PhotoPostForm
    # レンダリングするテンプレート
    template_name = 'post_photo.html'
    # フォームデータ登録完了後のリダイレクト先
    success_url = reverse_lazy('photo:post_done')

    def form_valid(self, form):
        '''CreateViewクラスのform_valid()をオーバーライド

        フォームのバリデーションを通過したときに呼ばれる
        フォームデータの登録をここで行う

        parameters:
            form(django.forms.Form):
                form_classに格納されているPhotoPostFromオブジェクト
        Return:
            HttpResponseRedirectオブジェクト:
                スーパークラスのform_valid()の戻り値を返すことで、success_urlで設定されているURLにリダイレクト
        '''
        # commit=FalseにしてPOSTされたデータを取得
        postdata = form.save(commit=False)
        # 投稿ユーザーのidを取得してモデルのuserフィールドに格納
        postdata.user = self.request.user
        # 投稿データをDBに登録
        postdata.save()
        # 戻り値はスーパークラスのform_valid()の戻り値(HttpResponseRedirect)
        return super().form_valid(form)


class PostSuccessView(TemplateView):
    '''投稿完了のページのビュー

    Attributes:
        template_name: レンダリングするテンプレート
    '''
    template_name = 'post_success.html'
