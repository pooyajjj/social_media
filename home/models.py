from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'posts')
    body = models.TextField()
    slug = models.SlugField()
    update = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta():
        ordering = ['-created','body']

    def __str__(self):
        return f'{self.slug}, {self.created}'  


    def get_absolute_url(self):
        return reverse('home:post_detail', args=(self.id, self.slug))

    def like_count(self):
        return self.pvotes.count()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'ucomments')
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'pcomments')
    reply = models.ForeignKey('Comment', on_delete = models.CASCADE, related_name = 'rcomments', blank = True, null = True)
    is_reply = models.BooleanField(default = False)
    body = models.TextField(max_length = 400)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self) :
        return f'{self.user} - {self.body[:30]}'


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uvotes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pvotes')


    def __str__(self):
        return f'{self.user} liked {self.post.slug}'