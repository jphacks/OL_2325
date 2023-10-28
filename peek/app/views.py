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

    #検索で得た場合
    if request.method == 'POST':
        users=request.POST['users']
        ulist = []
        for user in users:
            ulist.append(user)
        find =request.POST['find']
        msgs =get_user_message(ulist,None)
    else:
        msgs=get_message()
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

def favorite(request, favorite_id):
    favo_msg = Post.objects.get(id=favorite_id)
    is_favo = Favorite.objects.filter(user=request.user).filter(post=favo_msg).count()
    #いいねが既についていたら外す、ついていなければつける
    if is_favo>=1:
        # messages.success(request='既にメッセージはGoodしています。')
        defavo = Favorite.objects.filter(user=request.user).filter(post=favo_msg).first()
        defavo.delete()
        favo_msg.favorite_count -= 1
    else:
        favorite = Favorite()
        favorite.user =request.user
        favorite.post =favo_msg
        favorite.save()  
        favo_msg.favorite_count += 1
        # messages.success(request,'メッセージにgoodしました！')
    favo_msg.save()

    return redirect (to='/')

@login_required(login_url='/login/')
def profile(request,user_id):
    user =User.objects.filter(id=user_id).first()
    msgs=get_user_message([user],None)
    params = {
        'login_user':request.user,
        'contents':msgs,
        'user':user
    }
    return render(request,'app/profile.html',params)

# def message(request,msg_id):
#     params = {

#     }
#     return render(request,'sns/message.html',params)

def get_user_message(users,find):
    #TODO:usersに限るフィルタを追加する->した
    #すべてを取得するのに別に'get_message()'を使用

    if find == None:
        msgs = Post.objects.filter(author__in=users)[:100]
    else:
        msgs = Post.objects.filter(author__in=users).filter(body__contains=find)[:100]
    return msgs

def get_message():
    return Post.objects.all()[:100]