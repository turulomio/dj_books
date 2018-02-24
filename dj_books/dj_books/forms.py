from django.forms import ModelForm, SelectDateWidget

from django.contrib.auth.models import User
from books.models import Profile, Book,  Author

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        

class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].widget = SelectDateWidget()
    class Meta:
        model = Profile
        fields = ('language', 'birth_date')

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'year','author')

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ('name', 'family_name','birth', 'death')
