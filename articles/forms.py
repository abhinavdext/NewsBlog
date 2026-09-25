from django import forms

from .models import Article, Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your comment...',
                'rows': 4,
            }),
        }


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article

        fields = [
            'title',
            'content',
            'image',
            'category',
            'status',
        ]

        widgets = {

            'title': forms.TextInput(attrs={
                'placeholder': 'Enter article title',
            }),

            'content': forms.Textarea(attrs={
                'placeholder': 'Write your article content...',
                'rows': 12,
            }),

        }