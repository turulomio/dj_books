from django.forms import ModelForm
from django.contrib.auth.models import User
from books.models import Profile

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].widget.attrs['class']="datepicker"
    class Meta:
        model = Profile
        fields = ('language', 'birth_date')