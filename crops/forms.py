from django import forms

class CropSuggestionForm(forms.Form):
    location = forms.CharField(
        label='Location',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'input-field'})  # Add CSS class
    )
    nitrogen = forms.FloatField(
        label='Nitrogen (N)',
        widget=forms.TextInput(attrs={'class': 'input-field'})  # Add CSS class
    )
    phosphorus = forms.FloatField(
        label='Phosphorus (P)',
        widget=forms.TextInput(attrs={'class': 'input-field'})  # Add CSS class
    )
    ph = forms.FloatField(
        label='pH',
        widget=forms.TextInput(attrs={'class': 'input-field'})  # Add CSS class
    )
    rainfall = forms.FloatField(
        label='Rainfall (mm)',
        widget=forms.TextInput(attrs={'class': 'input-field'})  # Add CSS class
    )
