from django import forms

class SearchBar(forms.Form):
    search = forms.CharField()

class NewItem(forms.Form):
    title = forms.CharField()
    textarea = forms.CharField(widget=forms.Textarea(), label='')

class EditItem(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(), label='')