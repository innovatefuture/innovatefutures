from django import forms
from .models import River
from typing import List, Any, Dict


class CreateRiverForm(forms.ModelForm):
    class Meta:
        model = River
        fields: List[str] = ['title', 'description', 'tags', 'image']
        widgets = {
            'description': forms.Textarea(),
        }
