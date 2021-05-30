from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.forms import ModelForm

from .models import users, Questiones,questionnaire


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

    class Meta:
        model = users
        fields = ('FirstName', 'LastName', 'email', 'username', 'password1', 'password2', 'sex', 'DOB')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            users = users.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % users)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            users = users.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = users
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = users
        fields = (
            'FirstName',
            'LastName',
            'profile_image',
            'DOB',
            'Address',
            'Country',
            'City',
            'hide_email',
            'about_me',
            'PostalCode',
        )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            users = users.objects.exclude(pk=self.instance.pk).get(email=email)
        except users.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % users)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            users = users.objects.exclude(pk=self.instance.pk).get(username=username)
        except users.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)

    def save(self, commit=True):
        users = super(AccountUpdateForm, self).save(commit=False)
        users.profile_image = self.cleaned_data['profile_image']
        users.hide_email = self.cleaned_data['hide_email']
        users.FirstName = self.cleaned_data['FirstName']
        users.LastName = self.cleaned_data['LastName']
        users.DOB = self.cleaned_data['DOB']
        users.Address = self.cleaned_data['Address']
        users.Country = self.cleaned_data['Country']
        users.City  = self.cleaned_data['City']
        users.about_me  = self.cleaned_data['about_me']
        users.PostalCode  = self.cleaned_data['PostalCode']
        if commit:
            users.save()
        return users


class CreateQueForm(forms.ModelForm):
    class Meta:
        model = Questiones
        fields = ['question', 'option_one', 'option_two', 'option_three']

# class questionnaire(forms.ModelForm):
#     class Meta:
#         model = questionnaire
        # fields = ['question1', 'question2', 'question3', 'question4','question5','question6','question7']

    # selected_option = request.POST['form']
    # if selected_option == 'option1':
    #     Ans.question1 = 'yes'
    # elif selected_option == 'option2':
    #     Ans.question1 = 'no'
    # elif selected_option == 'option3':
    #     Ans.question1 = 'sometimes'
    # else:
    #     return HttpResponse(400, 'Invalid form option')