from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import Post, Author
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

class PostEconomics(ListView):
    template_name = 'news_by_category/economics.html'
    queryset = Post.objects.filter(category__name='economics')
    context_object_name = 'economic_news'
    ordering = ['-id']
    paginate_by = 10

class PostPolitics(ListView):
    template_name = 'news_by_category/politics.html'
    queryset = Post.objects.filter(category__name='politics')
    context_object_name = 'politics_news'
    ordering = ['-id']
    paginate_by = 10

class PostTechnologies(ListView):
    template_name = 'news_by_category/technologies.html'
    queryset = Post.objects.filter(category__name='technologies')
    context_object_name = 'technologies_news'
    ordering = ['-id']
    paginate_by = 10

class PostSport(ListView):
    template_name = 'news_by_category/sport.html'
    queryset = Post.objects.filter(category__name='sport')
    context_object_name = 'sport_news'
    ordering = ['-id']
    paginate_by = 10

class PostTourism(ListView):
    template_name = 'news_by_category/tourism.html'
    queryset = Post.objects.filter(category__name='tourism')
    context_object_name = 'tourism_news'
    ordering = ['-id']
    paginate_by = 10

class PostOpinions(ListView):
    template_name = 'news_by_category/opinions.html'
    queryset = Post.objects.filter(category__name='opinions')
    context_object_name = 'opinions_news'
    ordering = ['-id']
    paginate_by = 10

@login_required
def become_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(author=user)

    return redirect('/')

