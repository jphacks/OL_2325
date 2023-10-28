from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Post, Comment, Favorite

# ここから追加
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm

from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from .forms import SignUpForm


# Create your views here.

def index(request):
    params = {

    }
    return render(request,'app/index.html',params)

class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'app/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'app/login.html'

# class SignupView(CreateView):
#     """ ユーザー登録用ビュー """
#     form_class = SignUpForm # 作成した登録用フォームを設定
#     template_name = "app/signup.html" 
#     success_url = reverse_lazy("accounts:index") # ユーザー作成後のリダイレクト先ページ

#     def form_valid(self, form):
#         # ユーザー作成後にそのままログイン状態にする設定
#         response = super().form_valid(form)
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password")
#         user = authenticate(username=username, password=password)
#         login(self.request, user)
#         return response

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'app/signup.html', {'form': form})