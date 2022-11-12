from curses import meta
from django import forms
from .models import Post, Comment

class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control'})
        }

class CommentreplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control'})
        }


    # def setup(self, request, *args, **kwargs):
    #     self.post_instance = get_object_or_404(Post, pk = kwargs['post_id'], slug = kwargs['post_slug'])
    #     return super().setup(request, *args, **kwargs)

    
    # def get(self, request, *args, **kwargs):
    #     comments = self.post_instance.pcomments.filter(is_reply = False)
    #     return render (request, 'home/detail.html', {'post':self.post_instance, 'comments':comments, 'form':self.form_class})


    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     if form.is_valid:
    #         new_comment = form.save(commit=False)
    #         new_comment.user = request.user
    #         new_comment.post = self.post_instance
    #         new_comment.save()
    #         messages.success(request, 'your comment has been submited', 'success')
    #         return redirect('home:post_detail', self.post_instance.id, self.post_instance.slug)