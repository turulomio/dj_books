from django.forms import ModelForm
from books.models import Book, Valoration

from django import forms
        
class BookAddForm(ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'year', 'author')
        widgets = {'author': forms.HiddenInput()}
        
                
class ValorationAddForm(ModelForm):
    class Meta:
        model = Valoration
        fields = ('book', 'user', 'comment', 'valoration', 'read_start', 'read_end')
        widgets = {'book': forms.HiddenInput(), 'user':forms.HiddenInput()}
#        form.fields['read_start'].widget.attrs['class'] ='datepicker'
#        form.fields['read_end'].widget.attrs['class'] ='datepicker'}
