from django.shortcuts import render,get_object_or_404,redirect
from .models import Author,Article,Tag,Comment
from django.contrib.auth.models import User
from .forms import LoginForm,CommentForm,RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
import urllib.parse
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView,DetailView
# Create your views here.

def index(request):
    post_list=Article.objects.all()
    author=Author.objects.all()
    return render(request,'spiders/index.html',context={'post_list':post_list,'author':author})

class IndexView(ListView):
    model = Article
    template_name = 'spiders/index.html'
    context_object_name = 'post_list'
    paginate_by = 5

    def get_context_data(self,**kwargs):
        context=super(IndexView,self).get_context_data(**kwargs)
        # context['post_list']=Author.objects.all()
        context['loginform']=LoginForm()
        return context

def log_in(request):
    if request.method=='GET':
        form=LoginForm()
        return render(request,'spiders/login.html',{'form':form})
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['uid']
            password=form.cleaned_data['pwd']
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                url=request.POST.get('source_url','/spiders')
                return redirect(url)
            else:
                return render(request,'spiders/login.html',{'form':form,'error':"password or username is not ture!"})
        else:
            return render(request,'spiders/login.html',{'form':form})

@login_required
def log_out(request):
    url=request.POST.get('source_url','/spiders')
    logout(request)
    return redirect(url)

def detail(request,pk):
    post=get_object_or_404(Article,pk=pk)
    commentform=CommentForm()
    loginform=LoginForm()
    comments=post.comment_set.all()
    return render(request,'spiders/detail.html',context={
        'post':post,
        'commentform':commentform,
        'comments':comments,
        'loginform':loginform
        })

@login_required
def comment(request,pk):
    form=CommentForm(request.POST)
    url=urllib.parse.urljoin('/spiders/post/',pk)
    if form.is_valid():
        user=request.user
        # article=Article.objects.get(id=pk)
        new_comment=form.cleaned_data['comment']
        c=Comment(content=new_comment,article_id=pk)
        c.user=user
        c.save()
    return redirect(url)

def register(request):
    error1 = "This name is already exist"
    valid = "This name is valid"

    if request.method=='GET':
        form=RegisterForm()
        return render(request,'spiders/register.html',{'form':form})
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if request.POST.get('raw_username','erjgiqfv240hqp5668ej23foi')!='erjgiqfv240hqp5668ej23foi':
            try:
                user=User.objects.get(username=request.POST.get('raw_username',''))
            except ObjectDoesNotExist:
                return render(request,'spiders/register.html',{'form':form,'msg':valid})
            else:
                return render(request,'spiders/register.html',{'form':form,'msg':error1})
        else:
            if form.is_valid():
                username=form.cleaned_data['username']
                email=form.cleaned_data['email']
                password1=form.cleaned_data['password1']
                password2=form.cleaned_data['password2']
                if password1!=password2:
                    return render(request,'spiders/register.html',{'form':form,'msg':"two password is not equal"})
                else:
                    user=User(username=username,password=password1,email=email)
                    user.save()
                    return redirect('/spiders/login')
            else:
                return render(request,'spiders/register.html',{'form':form})

