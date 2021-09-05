from django.shortcuts import render
# TemplateView, CreateViewをインポート
from django.views.generic import TemplateView, CreateView, ListView, DetailView, DeleteView
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


class CategoryView(ListView):
    '''カテゴリページのビュー

    Attributes:
        template_name: レンダリングするテンプレート
        paginate_by: 1ページに表示するレコード件数
    '''
    template_name = 'index.html'
    paginate_by = 6

    def get_queryset(self):
        '''クエリの実行

        self.kwargsの取得が必要なので、クラス変数querysetではなく、get_queryset()のオーバーライド

        Returns:
            クエリによって取得されたレコード
        '''
        # self.kwargsでキーワードの辞書を取得し、categoryキーの値（Categorysテーブルのid）を取得
        category_id = self.kwargs['category']
        # filterで絞り込み
        categories = PhotoPost.objects.filter(
            category=category_id).order_by('-posted_at')
        # クエリの結果を返す
        return categories


class UserView(ListView):
    '''ユーザー投稿一覧ページのビュー

    Attributes:
        template_name: レンダリングするテンプレート
        paginate_by: 1ページに表示するレコード件数
    '''
    template_name = 'index.html'
    paginate_by = 6

    def get_queryset(self):
        '''クエリを実行する

        self.kwargsの取得が必要なため、get_queryset()のオーバーライド

        Returns:
            クエリによって取得されたレコード
        '''
        # self.kwargsからuserキーの値（「ユーザー」テーブルのid）を取得
        user_id = self.kwargs['user']
        # filterで絞り込み
        user_list = PhotoPost.objects.filter(
            user=user_id).order_by('-posted_at')
        # クエリの結果を返す
        return user_list


class DetailView(DetailView):
    '''詳細ページのビュー

    投稿記事の詳細を表示
    Attributes:
        template_name: レンダリングするテンプレート
        model: モデルクラス
    '''
    template_name = 'detail.html'
    model = PhotoPost


class MypageView(ListView):
    '''マイページのビュー

    Attributes:
        template_name: レンダリングするテンプレート
        paginate_by: 1ページに表示するレコード数
    '''
    template_name = 'mypage.html'
    paginate_by = 6

    def get_queryset(self):
        '''クエリを実行する

        self.kwargsの取得が必要なため、get_queryset()のオーバーライド

        Returns:
            クエリによって取得されたレコード
        '''
        # 現在ログインしているユーザー名はHttpRequest.userに格納されている
        # filter(userフィールド=userオブジェクト)で絞り込み
        queryset = PhotoPost.objects.filter(
            user=self.request.user).order_by('-posted_at')
        return queryset


class PhotoDeleteView(DeleteView):
    '''レコードの削除

    Attributes:
        model: モデル
        template_name: レンダリングするテンプレート
        paginate_by: 1ページに表示するレコード数
        success_url: 削除完了後のリダイレクト先
    '''
    # 操作対象はPhotoPostモデル
    model = PhotoPost
    # レンダリングするテンプレート
    template_name = 'photo_delete.html'
    # 削除完了後のリダイレクト先
    success_url = reverse_lazy('photo:mypage')

    def delete(self, request, *args, **kwargs):
        '''django.views.generic.edit.DeletionMixin.delete()のオーバーライド

            Parameters:
                self: PhotoDeleteViewオブジェクト
                request: WSGIRequest(HttpRequest)オブジェクト
                args: 引数として渡される辞書
                kwargs: キワード付き辞書
            
            Returns:
                HttpResponseRedirect(success_url)を返してsuccess_urlにリダイレクト
        '''
        return super().delete(request, *args, **kwargs)
