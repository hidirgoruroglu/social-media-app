from allauth.account.forms import LoginForm,SignupForm
from django.forms.widgets import HiddenInput

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({'class': 'bg-gray-200 mb-2 shadow-none dark:bg-gray-800"',})
        self.fields['password'].widget.attrs.update({'class': 'bg-gray-200 mb-2 shadow-none dark:bg-gray-800"',})
        self.fields['remember'].widget = HiddenInput()

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'bg-gray-200 mb-2 shadow-none dark:bg-gray-800"',})
        self.fields['email'].widget.attrs.update({'class': 'bg-gray-200 mb-2 shadow-none dark:bg-gray-800"',})
        self.fields['password1'].widget.attrs.update({'class': 'bg-gray-200 mb-2 shadow-none dark:bg-gray-800"',})
        self.fields['password2'].widget.attrs.update({'class': 'bg-gray-200 mb-2 shadow-none dark:bg-gray-800"',})


