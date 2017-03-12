from django import forms


# form data management
class LoginForm(forms.Form):
    id = forms.CharField(label="ID", max_length=12)
    password = forms.CharField(label="PASSWORD", max_length=12)


class JoinForm(forms.Form):
    id = forms.CharField(label="ID", min_length=4, max_length=12, required=True)
    password = forms.CharField(label="PASSWORD", min_length=6, max_length=12, required=True, widget=forms.PasswordInput)
    password_check = forms.CharField(label="PASSWORD(again)", min_length=6, max_length=12, required=True,
                                     widget=forms.PasswordInput)
