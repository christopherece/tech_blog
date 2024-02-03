from django.shortcuts import render
from django.http import HttpResponse
from posts.models import Category, Post
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.
def index(request):
    posts = Post.objects.order_by('-created_at').filter(is_published=True)
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    paged_posts = paginator.get_page(page)
    
    context = {
        'posts': paged_posts
    }
    return render(request, 'pages/index.html', context)

def about(request):
    return render(request, 'pages/about.html')

def contact(request):
    return render(request, 'pages/contact.html')
