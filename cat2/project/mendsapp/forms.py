from django import forms
from .models import ImageCategory, Image

class CategoryData(forms.ModelForm):
    class Meta:
        model = ImageCategory  # Use 'model' instead of 'data'
        fields = ['name']




class ImageData(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['name', 'file', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter image title', 'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),  # This will use the choices set in __init__
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get all categories and set choices for the dropdown
        categories = ImageCategory.objects.all()
        self.fields['category'].choices = [(cat.id, cat.name) for cat in categories]
