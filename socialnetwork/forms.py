from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email

from socialnetwork.models import Profile

MAX_UPLOAD_SIZE = 2500000

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length = 20)
    first_name=forms.CharField(max_length=50)
    last_name=forms.CharField(max_length=50)
    password = forms.CharField(max_length = 200)
    confirm_password = forms.CharField(max_length = 200)
    email=forms.CharField(max_length=200,validators = [validate_email])

    # Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        # Generally return the cleaned data we got from our parent.
        return cleaned_data

class EditProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        exclude={'account','followee','picture_url'}
    avatar = forms.FileField(required=False)

class AddPostForm(forms.Form):
    content=forms.CharField(max_length=160)

class AddReplyForm(forms.Form):
    post_id=forms.CharField()
    content=forms.CharField(max_length=160)