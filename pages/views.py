from django.shortcuts import render, redirect
from django.http import HttpResponse
from posts.models import Category, Post, Comment
from .models import Contact, Subscribe
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404

from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags



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


def subscribeme(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Check if email already exists
        if Subscribe.objects.filter(email=email).exists():
            messages.info(request, 'This email is already subscribed.')
        else:
            subscribeme = Subscribe(email=email)
            subscribeme.save()
            messages.success(request, 'Thank you! You are now subscribed.')
        
        return redirect('index')  # Redirect to 'index' or the appropriate URL name
    return render(request, 'index')
    

def submitcontact(request):
    categories = Category.objects.all().order_by('name')
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        description = request.POST['description']

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
        name = name,

    )

    contact.save()
    # Render the HTML template with context
    html_message = render_to_string('pages/emailtemplate.html', {'name': name})

        # Optionally, you can strip HTML tags for a plain text alternative
    plain_message = strip_tags(html_message)

        # Sending email
        
    recipient_list = [email]
    send_mail(
        'Thank you for contacting Us',
        'Email has been received and I will reply to you the soonest',  # Plain text version of the email
        'balaydalakay@gmail.com',  # From email address
        recipient_list,  # To email address(es)
        html_message=html_message,  # HTML version of the email
    )
    messages.success(request, 'Your message has been submitted')
    return render(request, 'pages/contact.html',{'categories':categories})

def about(request):
    categories = Category.objects.all().order_by('name')
    context = {
        'categories':categories
    }

    return render(request, 'pages/about.html', context)

def contact(request):    
    categories = Category.objects.all().order_by('name')
    context = {
        'categories':categories
    }
    return render(request, 'pages/contact.html', context)

