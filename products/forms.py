from django import forms
from .models import ContactMessage 
from django.contrib.auth.models import User


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الاسم'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ادخل بريدك الإلكتروني'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ادخل عنوان الرسالة'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'ادخل نص الرسالة'}),
        }