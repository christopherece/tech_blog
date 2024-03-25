from django.shortcuts import render, redirect
from django.http import HttpResponse
from posts.models import Category, Post
from .models import Contact
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages
from django.utils import timezone


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

def submitcontact(request):
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
    return render(request, 'pages/contact.html')

def about(request):
    return render(request, 'pages/about.html')

def contact(request):
    return render(request, 'pages/contact.html')
