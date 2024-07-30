from django.shortcuts import render, redirect
from django.http import HttpResponse
from posts.models import Category, Post
from .models import Contact
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from posts.models import Comment, Post



# Create your views here.
def index(request):
    # Fetch all categories
    categories = Category.objects.all().order_by('name')

    # Get all published posts
    posts = Post.objects.filter(is_published=True).order_by('-created_at')

    # Get the selected category ID from the query parameters
    category_id = request.GET.get('category')

    # If a category ID is provided, filter posts by that category
    if category_id:
        category = get_object_or_404(Category, pk=category_id)
        posts = posts.filter(categories=category)

    # Pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    paged_posts = paginator.get_page(page_number)

    context = {
        'posts': paged_posts,
        'categories': categories,
        'selected_category_id': category_id,
    }
    return render(request, 'pages/index.html', context)

def submitcontact(request):
    categories = Category.objects.all().order_by('name')
    if request.method == 'POST':
        description = request.POST['description']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

    # Check if the email is already exist
        # Check if the email and date combination already exists
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timezone.timedelta(days=1)
        if Contact.objects.filter(email=email, date__range=(today_start, today_end)).exists():
            messages.error(request, 'You have already submitted a message with this email today. Please wait for response!')
            return render(request, 'pages/contact.html')

    contact = Contact(
        description = description,
        email = email, 
        subject = subject,
        message = message,

    )

    contact.save()
    messages.success(request, 'Your message has been submitted')
    return render(request, 'pages/contact.html',{'categories':categories})

def about(request):
    categories = Category.objects.all().order_by('name')

    return render(request, 'pages/about.html',{'categories':categories})

def contact(request):    
    categories = Category.objects.all().order_by('name')
    return render(request, 'pages/contact.html',{'categories':categories})
