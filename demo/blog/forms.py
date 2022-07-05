from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class RegisterForm(UserCreationForm):
    # input
    username = forms.CharField(
    help_text='Необходимый. 150 символов или меньше. Только буквы, цифры и @ /. / + / - / _.',
    # minimalka
    min_length=8,  
    #maximalka
    max_length=150,
    # label 
    label = 'Логин', 
    # obezalovka
    required=True,  
    # 
    widget=forms.TextInput(attrs={'placeholder': 'никнейм', 'class':'form-control'})
    )

    password1 = forms.CharField(
        label='Пароль', 
        min_length=8, 
        required=True, 
        widget=forms.PasswordInput(attrs={'placeholder': '', 'class':'form-control'}))

    password2 = forms.CharField(
        label='Повторите пароль', 
        min_length=8, 
        required=True, 
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль', 'class':'form-control'}),
        help_text='Введите тот же пароль, что и раньше, для проверки.',
        )

    email = forms.EmailField(
        label='E-mail', 
        required=True, 
        widget=forms.EmailInput(attrs={'placeholder': 'ivan@gmail.com', 'class':'form-control'}))
    
    
    class Meta:
        model = User

        fields = ("email", "username", "password1", "password2",)


    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user    

    
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username
    

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email


    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2


