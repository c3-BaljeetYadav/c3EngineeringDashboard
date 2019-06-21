from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = ('username', 'email', 'GithubUser', 'password1', 'password2')
        labels = {
            'GithubUser': 'Github Username'
        }
