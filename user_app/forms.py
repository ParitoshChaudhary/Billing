from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django import forms
from user_app.models import Profile

User = get_user_model()

class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'username', 'phone', 'restraunt_name', 'password']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't mactch")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_admin', 'username', 'phone', 'restraunt_name')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=25, strip=True)
    email = forms.EmailField()
    phone = forms.IntegerField()
    restraunt_name = forms.CharField(max_length=40, strip=True)
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'phone', 'restraunt_name', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError('Username already exixts')
        return username

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', strip=True)
    password = forms.CharField(widget=forms.PasswordInput)
    
    
class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=25, strip=True)
    email = forms.EmailField()
    phone = forms.IntegerField()
    restraunt_name = forms.CharField(max_length=40, strip=True)
    
    class Meta:
        model = User
        fields = ('username', 'phone', 'restraunt_name', 'email')
        

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'address', 'manager_name', 'state_gst', 'centre_gst', 'add_tax']
