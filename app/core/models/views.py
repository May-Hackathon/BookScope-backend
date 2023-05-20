#認証機能
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RegistrationForm
from .forms import ProfileForm
from django.contrib.auth.tokens import default_token_generator

#ログイン情報取得
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone


def login_view(request):
    if request.method == 'POST':
        username = request.GET.get('username')
        password = request.GET.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            token = generate_token(user)
            return JsonResponse({'token': token})     #ログイン成功後のリダイレクト先を指定

        else:
            return JsonResponse({'error': 'ユーザ名またはパスワードが間違っています'})
    
    else:
        return render(request, 'login.html')    #login.htmlは仮
    


def generate_token(user):
    """
    ユーザに関連するトークンを生成、保存
    """
    token = default_token_generator.make_token(user)
    user.token = token
    user.save()



def logout_view(request):
    logout(request)
    return redirect('')     #ログアウト後のリダイレクト先を指定


#ユーザ登録機能
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.POST.get('username')
            password = form.POST.get('password')
            email = form.POST.get('email')
            User.objects.create_user(username=username, password=password, email=email)
            #登録完了後のリダイレクト先を指定
            return redirect('login.html')
        else:
            form = RegistrationForm()
        return render(request, 'register.html', {'form': form})



#アカウント情報管理機能
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            #プロフィール編集完了後のリダイレクト先を指定
            return redirect('profile.html')

        else:
            form = ProfileForm(instance=request.user.profile)
    # フォームの HTML レンダリング結果を取得        
    form_data = {'form': form.as_p()}
    return JsonResponse(form_data)
    


#ログイン情報取得
@login_required
def login_info(request):
    user = request.user
    login_time = user.last_login

    # フロントエンドに返すデータを作成
    data = {
        'username': user.username,
        'login_time': login_time.isoformat()
    }

    return JsonResponse(data)