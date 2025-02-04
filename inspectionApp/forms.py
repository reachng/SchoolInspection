from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
class InspectionForm(forms.ModelForm):
    class Meta:
        model = Inspection
        fields = [
            'school_name',
            'sf_code',
            'inspector_name',
            'photo',
            'question_1',
            'question_2',
            'question_3',
            'question_4',
            'question_5',
            'question_6',
            'question_7',
        ]
class LoginForm(AuthenticationForm):
    # You can customize the form here if needed
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    school_name = forms.CharField(max_length=255, required=True)
    is_inspector = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'school_name', 'is_inspector']

    def save(self, commit=True):
        # Save user information (including first_name, last_name)
        user = super().save(commit=False)
        if commit:
            user.save()

        # Create or update the UserProfile
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.school_name = self.cleaned_data['school_name']
        profile.is_inspector = self.cleaned_data['is_inspector']
        profile.save()

        return user

class InspectorRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
        
class InspectionForm(forms.ModelForm):
    class Meta:
        model = Inspection
        fields = ['school_name', 'sf_code', 'inspector_name', 'question_1', 'question_2', 'question_3', 'question_4', 'question_5', 'question_6', 'question_7', 'photo']

    # Custom widget for better mobile UI
    question_1 = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}))
    question_2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    photo = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))