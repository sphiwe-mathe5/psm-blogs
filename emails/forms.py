from django import forms
from .models import EmailTemplate


class EmailForm(forms.Form):
    recipient = forms.CharField(widget=forms.Textarea, help_text="Enter multiple emails separated by commas")
    template = forms.ModelChoiceField(queryset=EmailTemplate.objects.all())
