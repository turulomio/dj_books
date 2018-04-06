import datetime
from django.forms import ModelForm, SelectDateWidget

from django.contrib.auth.models import User
from books.models import Profile, Book,  Author, Valoration

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        

class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        sdw=SelectDateWidget()
        sdw.years=range(1900, datetime.date.today().year+1)
        self.fields['birth_date'].widget = sdw
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

class ValorationForm(ModelForm):
    class Meta:
        model = Valoration
        fields = ('book', 'user', 'comment','valoration','read_start','read_end')
