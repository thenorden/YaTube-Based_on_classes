from django import forms
from django.forms import Textarea

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'text': 'Комментарий'
        }
        widgets = {
            'text': Textarea(attrs={'rows': 3})
        }

    def clean(self):
        data = super().clean()

        text = data.get('text')
        for word in text:
            if word in '123456789':
                raise forms.ValidationError('Цифры нельзя')

        return data




