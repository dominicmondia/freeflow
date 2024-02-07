from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import UserProfile


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)

        # create empty user profile upon user creation
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            user_profile, created = UserProfile.objects.get_or_create(user=user)  # modified line
            if created:
                # If you need to initialize any fields when the UserProfile is first created, do so here
                # user_profile.field = value
                user_profile.save()
        return user
