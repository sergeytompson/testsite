from django import forms
from .models import Category, News, Comments
from django.core.exceptions import ValidationError


class NewsForm(forms.Form):
    title = forms.CharField(max_length=150, label='Заголовок',
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Текст новости', required=False,
                              widget=forms.Textarea(attrs={'class': 'form-control'}))
    is_publish = forms.BooleanField(label='Опубликовать', initial=True, required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      label='Категория',
                                      empty_label='Выберете категорию',
                                      widget=forms.Select(attrs={'class': 'form-control'}))


class NewsFormFromModel(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'is_publish', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if title[0].isdigit():
            raise ValidationError('Название не должно наианяться с цифры')
        return title


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['username', 'text']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control',
                                          'rows': 5})
        }
