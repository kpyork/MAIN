from django.shortcuts import redirect, render, get_object_or_404
from .models import Author, Category, Post,Comment,Reply
from .utils import update_views
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
def home(request):
    forums = Category.objects.all()
    num_posts = Post.objects.all().count()
    num_users = User.objects.all().count()
    num_categories = forums.count()
    try:
        last_post = Post.objects.latest("date")
    except:
        last_post = []
    context = {
        'forums': forums,
        'num_posts': num_posts,
        'num_users': num_users,
        'num_categories': num_categories,
        'last_post': last_post,
        'title': "Home Page",
        
    }
    return render(request, "home.html", context)

def posts(request,slug):
    category = get_object_or_404(Category,slug=slug)
    posts = Post.objects.filter(approved = True,categories = category)
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page) #returns Page object
    except PageNotAnInteger:
        posts = paginator.page(1) # If page is not an integer deliver the first page
    except EmptyPage:
        posts = paginator.page(paginator.num_pages) # If page is out of range deliver last page of results
    context = {
        'posts': posts,
        'forum' : category,
        'title' : "Posts"
        
    }
    return render(request, "posts.html", context)

def detail(request,slug):
    post = get_object_or_404(Post, slug = slug)
    if request.user.is_authenticated:
        author  = Author.objects.get(user = request.user)

    if "comment-form" in request.POST:
        comment = request.POST.get("comment")
        new_comment,created = Comment.objects.get_or_create(user=author,content=comment)
        post.comments.add(new_comment.id) #linking comment to post

    if "reply-form" in request.POST:
        reply = request.POST.get("reply")
        commenr_id = request.POST.get("comment-id")
        comment_obj = Comment.objects.get(id=commenr_id)
        new_reply,created = Reply.objects.get_or_create(user=author,content=reply)
        comment_obj.replies.add(new_reply.id)

    context = {
        'post': post,
        'title': post.title,
    }
    update_views(request, post)
    return render(request, "detail.html", context)



@login_required
def create_post(request):
    context = {}
    form = PostForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            author = Author.objects.get(user = request.user)
            new_post = form.save(commit = False)
            new_post.user = author
            new_post.slug = slugify(new_post.title)
            new_post.save()
            form.save_m2m()
            return redirect("home")
    context.update({
        'form': form,
        'title': "Create Post",
    })
    return render(request, "create_post.html", context)



def latest_posts(request):
    posts = Post.objects.all().filter(approved = True)[:10]
    context = {
        'posts': posts,
        'title': "Last 10 Posts",
    }
    return render(request, "latest_posts.html", context)

def search_result(request):
    return render(request, "search_result.html")