from django.shortcuts import render, redirect
from django.views import View
from home.forms import PostCreateUpdateForm, CommentCreateForm, CommentreplyForm
from .models import Post, Comment, Vote
from django.contrib.auth.mixins import  LoginRequiredMixin
from django.contrib import messages
from django.utils.text import slugify
from django.shortcuts import get_object_or_404



class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render (request, 'home/index.html', {'posts':posts})


class PostDetailView(View):
    form_class = CommentCreateForm
    form_class_reply = CommentreplyForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk = kwargs['post_id'], slug = kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    
    def get(self, request, *args, **kwargs):
        comments = self.post_instance.pcomments.filter(is_reply = False)
        return render (request, 'home/detail.html', {'post':self.post_instance, 'comments':comments, 'form':self.form_class, 'relpy_form':self.form_class_reply})


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid:
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, 'your comment has been submited', 'success')
            return redirect('home:post_detail', self.post_instance.id, self.post_instance.slug)


class PostDeleteView(LoginRequiredMixin, View):

    def get(self, request, post_id):
        post = Post.objects.get(pk = post_id)
        if post.user.id == request.user.id :
            post.delete()
            messages.success(request, 'post deleted successfully', 'success')
        else:
            messages.error(request, "you can't delete this post", 'danger')

        return redirect('account:user_profile', post.user.id)


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk = kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, "you can't update this post", 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'home/update.html', {'form':form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'update succssfully', 'success')
            return redirect('home:post_detail', post.id, post.slug)



class PostCreateView(LoginRequiredMixin ,View):
    form_class = PostCreateUpdateForm


    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, 'home/create.html', {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'your post has been created', 'success')
            return redirect('home:post_detail', new_post.id, new_post.slug)



class PostAddReplyView(LoginRequiredMixin, View):
    form_class = CommentreplyForm


    # def setup(self, request, *args, **kwargs):
    #     self.post_instance = Comment.objects.get(pk = kwargs['post_id'], comment = kwargs['comment_id'])
    #     return super().setup(request, *args, **kwargs)


    def post(self, request, post_id, comment_id):
        post = get_object_or_404(Post, id = post_id)
        comment = get_object_or_404(Comment, id=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, 'your reply submited', 'success')
        return redirect('home:post_detail', post.id, post.slug )


class PostLikeView(LoginRequiredMixin, View):

    def get(self, request, post_id):
        post = get_object_or_404(Post, id = post_id)
        like = Vote.objects.filter(post=post, user=request.user)

        if like.exists():
            messages.error(request, 'You already liked this post', 'danger')

        else:
            Vote.objects.create(post=post, user=request.user)
            messages.success(request, 'You liked the post', 'success')

        return redirect('home:post_detail', post.id, post.slug)