from django import forms
from .models import Post, PostComment
from legend_blog.models import PostReaction


class RateForm(forms.ModelForm):
    rate = forms.ChoiceField(choices=PostReaction.RATE_OPTIONS, help_text='Оставьте реакцию',
                             widget=forms.Select(attrs={'class': 'form-select', 'aria-label': 'Default select example'}))

    class Meta:
        model = PostReaction
        fields = ("rate",)


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "text", "thumbnail", "status")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class": 'form-control',
                'autocomplete': "off"
            })


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "text", "thumbnail", "status")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class": 'form-control',
                'autocomplete': "on"
            })


class CommentForm(forms.ModelForm):
    nickname = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Name"}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}))
    body = forms.CharField(required=True,
                           widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Text", "style": "height: 150px;"}))

    class Meta:
        model = PostComment
        fields = ('nickname', 'email', 'body')
