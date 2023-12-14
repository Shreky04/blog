import datetime

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.timezone import now

from .forms import PostForm, CommentsForm, SubscribeForm, UserProfileCreationForm
from .models import Post, Category, Tag, Comments, UserProfile


# Create your views here.

def get_categories():
    all = Category.objects.all()
    count = all.count()
    return{'cat1':all[ :count/2 + count%2], 'cat2':all[count/2+count%2 : ]}


def index(request):
    posts = Post.objects.all().order_by("-published_date")
    #posts = Post.objects.all()
    #post_id = Post.objects.get(pk=1)
    #posts = Post.objects.filter(title__contains="js")
    #posts = Post.objects.filter(published_date__year = 2023)
    #posts = Post.objects.filter(category__name__iexact="C")
    #categories = Category.objects.all()
    #post_tags = Tag.objects.all()

    context = {"posts":posts}
    context.update(get_categories())
    return render(request, 'blog/index.html', context=context)

def post(request, id=None):
    post = get_object_or_404(Post, title=id)
    comment_form=CommentsForm()
    comments = Comments.objects.filter(post=post).order_by('-published_date')
    if request.method=="POST":
        form=CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated:
                comment.author = request.user
            else:
                return redirect(reverse('signup'))
            comment.published_date = now()
            comment.save()
            return render(request, 'blog/post.html', context={'post':post, 'comments_form':comment_form, 'comments':comments})
    context = {"post":post, 'comments_form':comment_form, 'comments':comments}
    context.update(get_categories())
    return render(request, 'blog/post.html', context=context)


def about(request):

    context = {}
    return render(request, 'blog/about.html', context=context)

def services(request):

    context = {}
    return render(request, 'blog/services.html', context=context)

def contact(request):

    context = {}
    return render(request, 'blog/contact.html', context=context)


def category(request, name=None):
    c = get_object_or_404(Category, name=name)
    posts = Post.objects.filter(category=c).order_by('-published_date')
    context={
        'posts':posts
    }
    context.update(get_categories())
    return render(request, 'blog/index.html', context=context)


def search(request):
    query = request.GET.get('query')
    posts = Post.objects.filter(Q(content__icontains=query)|Q(title__icontains=query)).order_by("-published_date")
    context = {"posts": posts}
    context.update(get_categories())
    return render(request, 'blog/index.html', context=context)

def tag(request, name=None):
    t = get_object_or_404(Tag, name=name)
    posts = Post.objects.filter(tag=t).order_by('-published_date')
    context={
        'posts':posts
    }
    context.update(get_categories())
    return render(request, 'blog/index.html', context=context)

@login_required
def create(request):
    if request.method=="POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date=now()
            post.user = request.user
            post.save()
            return index(request)
    form = PostForm()
    context = {"form" : form}
    context.update(get_categories())
    return render(request, 'blog/create.html', context=context)


def user_logout(request):
    logout(request)
    return redirect('index')

def subscribe(request):
    form = SubscribeForm()
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    return render(request, 'blog/subscription.html', {'form': form})


def success(request):
    return render(request, 'blog/success.html')


def signup(request):
    if request.method == 'POST':
        form = UserProfileCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            UserProfile.objects.create(user=user, phone=form.cleaned_data['phone'],
                                       dateofbirth=form.cleaned_data['dateofbirth'])
            auth_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, auth_user)

            return redirect('index')
    else:
        form = UserProfileCreationForm()

    return render(request, 'registration/signup.html', {'form': form})