

from django import forms
from django.contrib.auth import get_user_model

from app_user.models import UserModel

User = get_user_model()
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields must match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password1']:
            user.set_password(self.cleaned_data['password1'])  # Set the password for the user
        if commit:
            user.save()
        return user
