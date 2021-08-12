# UserCreationFormクラスをインポート
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
# models.pyで定義したカスタムUserモデルをインポート


class CustomUserCreationForm(UserCreationForm):
    '''UserCreationFormのサブクラス
    '''
    class Meta:
        '''UserCreationFormのインナークラス

        Attributes:
          model:連携するUserモデル
          fields:フォームで使用するフィールド
        '''
        # 連携するUserモデルの設定
        model = CustomUser
        # フォームで使用するフィールド(ユーザ名、メアド、パス、パス(確認用))
        fields = ('username', 'email', 'password1', 'password2')
