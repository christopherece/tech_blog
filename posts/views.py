from django.shortcuts import render, redirect, get_object_or_404

from .models import Post, Comment, Category
from .forms import CommentForm

# Create your views here.


def post(request, post_id):

    post = get_object_or_404(Post, pk=post_id)
    total_comments = Comment.objects.filter(post=post).count()
    comments = Comment.objects.filter(post=post)
    categories = Category.objects.all().order_by('name')

    # Fetch the next and previous posts based on the creation date
    next_post = Post.objects.filter(created_at__gt=post.created_at).order_by('created_at').first()
    previous_post = Post.objects.filter(created_at__lt=post.created_at).order_by('-created_at').first()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            # Redirect back to the same page after successfully posting a comment
            return redirect(request.path)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'categories':categories,
        'next_post': next_post,
        'previous_post': previous_post,
        'total_comments': total_comments,
        'comments': comments,
        'form': form,
    }

    return render(request, 'posts/post.html', context)

def search(request):

    return render(request, 'posts/search.html')
