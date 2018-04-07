import datetime
from django.forms import ModelForm, SelectDateWidget, DateField

from django.contrib.auth.models import User
from books.models import Profile, Book,  Author, Valoration
from django.contrib.admin.widgets import AdminDateWidget

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

"""
class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'year','author')

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ('name', 'family_name','birth', 'death')

class ValorationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ValorationForm, self).__init__(*args, **kwargs)
        print(self.fields)
        self.fields['read_end'].widget.attrs['class'] = 'datepicker'
        self.fields['read_start'].widget.attrs['class'] = 'datepicker'
    class Meta:
        model = Valoration
                fields = ('book', 'user', 'comment','valoration','read_start','read_end')
            """