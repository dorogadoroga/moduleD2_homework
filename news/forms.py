from django.forms import ModelForm
from .models import Post, PostCategory

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'is_news', 'title', 'text', 'category']

