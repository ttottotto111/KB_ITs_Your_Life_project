from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        exclude=('post','author','created_at','modified_at')
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'든든하게 입력해주세요'})}