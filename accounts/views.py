from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Blog
from django.contrib import messages
from django.utils.text import slugify


def register_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, 'register.html')
        
        user = User(full_name=full_name, email=email)
        user.set_password(password)
        user.save()

        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    return render(request, 'login.html')

@login_required
def dashboard_view(request):
    return render(request, 'blog_list.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# Blog Views
def blog_list(request):
    blogs = Blog.objects.filter(status='published')
    return render(request, 'blog_list.html', {'blogs': blogs})

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, status='published')
    return render(request, 'blog_detail.html', {'blog': blog})

@login_required
def create_blog(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES.get('image')
        status = request.POST['status']
        blog = Blog.objects.create(title=title, content=content, image=image, status=status, author=request.user)
        return redirect('blog_list')
    return render(request, 'create_blog.html')

@login_required
def edit_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if blog.author != request.user:
        return redirect('blog_list')
    
    if request.method == 'POST':
        blog.title = request.POST['title']
        blog.content = request.POST['content']
        blog.status = request.POST['status']
        if 'image' in request.FILES:
            blog.image = request.FILES['image']
        blog.save()
        return redirect('blog_detail', slug=blog.slug)
    return render(request, 'edit_blog.html', {'blog': blog})

@login_required
def delete_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if blog.author == request.user:
        blog.delete()       
    return redirect('blog_list')

@login_required
def profile(request):
    user_blogs = Blog.objects.filter(author=request.user)
    return render(request, 'profile.html', {'blogs': user_blogs})
    