from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages

# ここから追加

from .models import Post, Comment, Favorite
from .forms import LoginForm,SignUpForm,PostForm

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView

from django.db.models import Q



# Create your views here.

def index(request):
    msgs =get_your_message(request.user,None)
    params = {
        'login_user':request.user,
        'contents':msgs
    }
    return render(request,'app/index.html',params)

class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'app/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'app/login.html'

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

@login_required(login_url='/login/')
def post(request):
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        image = request.FILES["image"]
        # Messageの作成、設定、保存
        msg = Post()
        msg.author = request.user
        msg.title = title
        msg.body = body
        msg.img = image
        msg.save()
        # messages.success(request, '新しいメッセージを投稿しました！')
        return redirect(to='/')
    #GETアクセス時の処理
    else:
        form= PostForm(request.user)
    #共通処理
    params = {
        'login_user':request.user,
        'form':form,
    }
    return render(request, 'app/postimg.html',params)

# def message(request,msg_id):
#     params = {

#     }
#     return render(request,'sns/message.html',params)

def get_your_message(owner,find):
    #TODO:ownerのfollowerに限るフィルタを追加する

    if find == None:
        msgs = Post.objects.all()[:100]
    else:
        msgs = Post.objects.filter(body__contains=find)[:100]
    return msgs
