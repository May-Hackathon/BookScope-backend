#認証機能
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RegistrationForm
from .forms import ProfileForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('')     #ログイン成功後のリダイレクト先を指定

        else:
            return render(request, 'login.html', {'error': 'ユーザ名またはパスワードが間違っています'})
    
    else:
        return render(request, 'login.html')    #login.htmlは仮


def logout_view(request):
    logout(request)
    return redirect('')     #ログアウト後のリダイレクト先を指定


#ユーザ登録機能
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            User.objects.create_user(username=username, password=password, email=email)
            #登録完了後のリダイレクト先を指定
            return redirect('login')
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
        return render(request,'profile_edit.html', {'form': form})
