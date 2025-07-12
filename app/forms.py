from django import forms
from .models import ProductReview

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your review here...'}),
        }
