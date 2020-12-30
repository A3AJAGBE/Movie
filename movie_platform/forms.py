from django import forms
from django.forms import ModelForm
from .models import Contact, Review


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Coupon Code'
    }))


class ContactForm(ModelForm):

    class Meta:
        model = Contact
        exclude = ('Reply',)


class ReviewForm(ModelForm):

    class Meta:
        model = Review
        exclude = ('Author', 'Posted', 'Movie')