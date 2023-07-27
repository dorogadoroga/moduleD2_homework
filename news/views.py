from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from datetime import datetime

from .models import *
from .filters import PostFilter
from .forms import PostForm


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    ordering = ['-id']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['is_not_login'] = not self.request.user.is_authenticated
        return context

class PostSearh(ListView):
    model = Post
    template_name = 'search.html'
    ordering = ['-id']


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'add.html'
    form_class = PostForm
    permission_required = 'news.add_post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        date = datetime.utcnow().strftime('%d %m %y')
        author = Author.objects.get(author=self.request.user)
        posts = Post.objects.filter(author=author).order_by('-date')[:3]
        if posts.count() >= 3:
            if all([post.date.strftime('%d %m %y') == date for post in posts]):
                context['limit_exceeded'] = True
        return context

    def post(self, request, *args, **kwargs):
        new_post = Post(
            author=Author.objects.get(author=request.user),
            title=request.POST['title'],
            text=request.POST['text'],
        )

        categories = request.POST.getlist('category')
        if 'is_news' in request.POST:
            new_post.is_news = True
        new_post.save()
        new_post.category.set(categories)
        new_post.save()

        # for cat in categories:
        #     category = Category.objects.get(id=cat)
        #     for user in category.subscribers.all():
        #         html_content = render_to_string('mail/post_for_send.html', {'new_post': new_post, 'user': user})
        #         msg = EmailMultiAlternatives(
        #             subject=new_post.title,
        #             body=new_post.text,
        #             to=[user.email]
        #         )
        #         msg.attach_alternative(html_content, "text/html")
        #         msg.send()

        return redirect('/')

class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'edit.html'
    form_class = PostForm
    permission_required = 'news.change_post'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/'
    permission_required = 'news.delete_post'


class PostsByCategory(ListView):
    template_name = 'category.html'
    model = Post
    context_object_name = 'news_by_categories'
    ordering = ['-id']
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        category = self.request.path.split('/')[-1]
        queryset = Post.objects.filter(category__slug=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        cat_slug = self.request.path.split('/')[-1]
        category = Category.objects.get(slug=cat_slug)
        context['category'] = category
        if user.is_authenticated:
            context['is_not_login'] = False
            context['subscribed'] = category.subscribers.filter(email=user.email)
        else:
            context['is_not_login'] = True
            context['subscribed'] = False
        return context

@login_required
def become_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(author=user)

    return redirect('/')

@login_required
def become_subscriber(request, slug, **kwargs):
    user = request.user
    category = Category.objects.get(slug=slug)
    subscribers = category.subscribers.all()
    if user not in subscribers:
        UserCategory.objects.create(user=user, category=category)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def delete_subscription(request, slug, **kwargs):
    user = request.user
    category = Category.objects.get(slug=slug)
    subscribers = category.subscribers.all()
    if user in subscribers:
        UserCategory.objects.get(user=user, category=category).delete()
    return redirect(request.META.get('HTTP_REFERER'))

