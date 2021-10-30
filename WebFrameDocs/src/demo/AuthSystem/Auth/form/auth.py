from django.forms import ModelForm

from Auth.models import User


class UserInfoForm(ModelForm):
    class Meta:
        model = User
        fields = ["is_developer"]
