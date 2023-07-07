from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.author.username}'


    def update_rating(self):
        post_rating = self.post_set.all().aggregate(postRating=Sum('rating'))
        p_r = post_rating.get('postRating') * 3
        author_comment_rating = self.author.comment_set.all().aggregate(authorCommentRating=Sum('rating'))
        a_c_r = author_comment_rating.get('authorCommentRating')
        post_comment_rating = Comment.objects.filter(post__author=self).values('rating').aggregate(
            postCommentRating=Sum('rating'))
        p_c_r = post_comment_rating.get('postCommentRating')
        self.rating = p_r + a_c_r + p_c_r
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    is_news = models.BooleanField(default=False)  # news=True, article=False
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    category = models.ManyToManyField(Category, through='PostCategory')

    def __str__(self):
        return f'{self.title[:10]}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:123] + '...'

    def get_absolute_url(self):
        return f'/news/{self.id}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET('Удаленный пользователь'))
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.text[:10]}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
