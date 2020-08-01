from django import forms


class NewPostForm(forms.Form):
    newpost = forms.CharField(label="newpost")
