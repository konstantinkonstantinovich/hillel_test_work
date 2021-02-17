from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from .models import Post


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size': '40', 'class': 'form-control'}))
    sender = forms.EmailField(widget=forms.TextInput(attrs={'size': '40', 'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))


class PostModelForm(forms.ModelForm):
    text = forms.CharField(label='Text', widget=forms.Textarea(attrs={'class': 'ckeditor'}))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'ckeditor'}))

    class Meta:
        model = Post
        fields = ["status", "title", "description", "text", "image"]
