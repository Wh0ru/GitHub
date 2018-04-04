from django.shortcuts import render,get_object_or_404,redirect
from .models import Article,Comment,Poll,NewUser
from .forms import LoginForm,CommentForm,RegisterForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import  ObjectDoesNotExist
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
import markdown2
import urllib.parse
from django.views.decorators.cache import cache_page
# Create your views here.

def index(request):
    latest_article_list=Article.objects.query_by_time()
    loginform=LoginForm()
    context={'latest_article_list':latest_article_list,'loginform':loginform}
    return render(request,'focus/index.html',context)

def log_in(request):
    if request.method=='GET':
        form= LoginForm()
        return render(request,'focus/login.html',{'form':form})
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['uid']
            password=form.cleaned_data['pwd']
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                url=request.POST.get('source_url','/focus')
                return redirect(url)
            else:
                return render(request,'focus/login.html',{'form':form,'error':"password or username is not ture!"})
        else:
            return render(request,'focus/login.html',{'form':form})

@login_required
def log_out(request):
    url=request.POST.get('source_url','/focus')
    logout(request)
    return redirect(url)

def article(request,article_id):
    article=get_object_or_404(Article,id=article_id)
    content=markdown2.markdown(article.content,extras=["code-friendly",
            "fenced-code-blocks","header-ids","toc","metadata"])
    commentform=CommentForm()
    loginform=LoginForm()
    comments=article.comment_set.all

    return render(request,'focus/article_page.html',{
        'article':article,
        'loginform':loginform,
        'commentform':commentform,
        'content':content,
        'comments':comments
    })

@login_required
def comment(request,article_id):
    form=CommentForm(request.POST)
    url=urllib.parse.urljoin('/focus/',article_id)
    if form.is_valid():
        user=request.user
        article=Article.objects.get(id=article_id)
        new_comment=form.cleaned_data['comment']
        c=Comment(content=new_comment,article_id=article_id)
        c.user=user
        c.save()
        article.comment_num+=1
    return redirect(url)

@login_required
def get_keep(request,article_id):
    logged_user=request.user
    article=Article.objects.get(id=article_id)
    articles=logged_user.article_set.all()
    if article not in articles:
        article.user.add(logged_user)
        article.keep_num+=1
        article.save()

        return redirect('/focus/')
    else:
        url=urllib.parse.urljoin('focus/',article_id)
        return redirect(url)

@login_required
def get_poll_article(request,article_id):
    logged_user=request.user
    article=Article.objects.get(id=article_id)
    polls=logged_user.poll_set.all()
    articles=[]
    for poll in polls:
        articles.append(poll.article)

    if article in articles:
        url=urllib.parse.urljoin('/focus/',article_id)
        return redirect(url)
    else:
        article.poll_num+=1
        article.save()
        poll=Poll(user=logged_user,article=article)
        poll.save()
        data={}
        return redirect('/focus/')

def register(request):
    error1="This name is already exist"
    valid="This name is valid"

    if request.method == 'GET':
        form=RegisterForm()
        return render(request,'focus/register.html',{'form':form})
    if request.method == 'POST':
        form=RegisterForm(request.POST)
        if request.POST.get('raw_username','erjgiqfv240hqp5668ej23foi')!='erjgiqfv240hqp5668ej23foi':
            try:
                user=NewUser.objects.get(username=request.POST.get('raw_username',''))
            except ObjectDoesNotExist:
                return render(request,'focus/register.html',{'form':form,'msg':valid})
            else:
                return render(request,'focus/register.html',{'form':form,'msg':error1})

        else:
            if form.is_valid():
                username=form.cleaned_data['username']
                email=form.cleaned_data['email']
                password1=form.cleaned_data['password1']
                password2=form.cleaned_data['password2']
                if password1 != password2:
                    return render(request,'focus/register.html',{'form':form,'msg':"two password is not equal"})
                else:
                    user=NewUser(username=username,email=email,password=password1)
                    user.save()
                    return redirect('/focus/login')
            else:
                return render(request,'focus/register.html',{'form':form})
