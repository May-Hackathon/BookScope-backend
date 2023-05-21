#認証機能
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RegistrationForm
from .forms import ProfileForm
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView

#ログイン情報取得
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone

class LoginView(APIView):
    def login_view(self, request):
        if request.method == 'POST':
            email = request.data.get('email')
            password = request.data.get('password')
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                token = generate_token(user)
                return JsonResponse({'token': token})

            else:
                return JsonResponse({'error': 'Incorrect email address or password'})
        
        else:
            return JsonResponse({'message': 'login successed'})
        


def generate_token(user):
    """
    ユーザに関連するトークンを生成、保存
    """
    token = default_token_generator.make_token(user)
    user.token = token
    user.save()



def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'logout'})


#ユーザ登録機能
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.POST.get('username')
            password = form.POST.get('password')
            email = form.POST.get('email')
            User.objects.create_user(username=username, password=password, email=email)
            return JsonResponse({'message':'Registration successful'})
        
        else:
            form = RegistrationForm()
        return JsonResponse({'form': form})



#アカウント情報管理機能
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return JsonResponse({'message':'Profile updated successfully'})

        else:
            form = ProfileForm(instance=request.user.profile)
    # フォームの HTML レンダリング結果を取得        
    form_data = {'form': form.as_p()}
    return JsonResponse(form_data)
    


#ログイン情報取得
@login_required
def user_login_info(request):
    user = request.user

    # フロントエンドに返すデータを作成
    login_info = {
        'username': user.username,
        'email':user.email,
        'last_login':user.last_login,
        'date_joined':user.date_joined,
        'login_history':[]
    }
    login_history = User.objects.filter(username=user.username).value('last_login')
    for login in login_history:
        login_info['login_history'].append(login['last_login'])

    return JsonResponse(login_info)