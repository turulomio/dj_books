
from django import forms
from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render,  get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from books.forms import BookAddForm, ValorationAddForm
from books.models import Author,  Book, Valoration
from books.tables import TableEasyAuthors,  TableEasyValorations, TableEasyBooks



def error_403(request, exception):
        data = {}
        return render(request,'403.html', data)

## @todo Add search to search field to repeat search
## @todo Limit search minimum 3 and maximum 50
## @todo Add a tab Widget, author, books, valorations with number in ttab
def home(request):
    search = request.GET.get('search')
    if search!=None:
        searchtitle=_("Looking for '{}' in Library database").format(search)
        books=Book.objects.filter(Q(title__icontains=search) | Q(year__icontains=search))
        authors=Author.objects.filter(Q(name__icontains=search) | Q(family_name__icontains=search))
        if request.user.has_perm('books.search_valoration'):
            valorations=Valoration.objects.filter(comment__icontains=search)
    return render(request, 'home.html', locals())
    

@permission_required('books.statistics_global')
def statistics_global(request):
    books= Book.objects.count()
    authors= Author.objects.count()
    valorations= Valoration.objects.count()
    return render(request,  "statistics_global.html", locals())    


@permission_required('books.statistics_user')
def statistics_user(request):
    valorations_number= Valoration.objects.filter(user=request.user).count()
    return render(request,  "statistics_user.html", locals())

@permission_required('books.database_all_view')
def database(request):
    authors= Author.objects.order_by('name')
    books=Book.objects.order_by('title')
    valorations=Valoration.objects.order_by('read_end')
    tableeasy_authors=TableEasyAuthors(authors, request)
    tableeasy_books=TableEasyBooks(books, request)
    tableeasy_valorations=TableEasyValorations(valorations, request)
    return render(request, 'database.html', locals())

@login_required
def valoration_list(request):
    valorations= Valoration.objects.filter(user=request.user).order_by('read_start')
    return render(request, 'valoration.html', locals())
    
def valoration_read(request, valoration_id):
    valoration=get_object_or_404(Valoration, pk=valoration_id)
    return render(request, 'books/valoration_read.html', locals())

def book_read(request, pk):
    book=get_object_or_404(Book, pk=pk)
    valorations=Valoration.objects.filter(book=book)
    return render(request, 'books/book_read.html', locals())
    
def author_read(request, pk):
    author=get_object_or_404(Author, pk=pk)
    books=Book.objects.filter(author=author)
    return render(request, 'books/author_read.html', locals())
    
@permission_required('books.add_book')
def book_new(request, author_id):
    author=get_object_or_404(Author, pk=author_id)
    if request.method == 'POST':
        form = BookAddForm(request.POST)
        if form.is_valid():
            book=Book()
            book.title= form.cleaned_data['title']
            book.author= author
            book.year= form.cleaned_data['year']
            book.save()
            return HttpResponseRedirect( reverse_lazy('author-read',args=(author_id,)))
    else:
        form = BookAddForm()
        form.fields['author'].initial=author
    return render(request, 'books/book_edit.html', {'form': form})
    
@permission_required('books.add_valoration')
def valoration_new(request, book_id):
    book=get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = ValorationAddForm(request.POST)
        if form.is_valid():
            valoration=Valoration()
            valoration.book=book
            valoration.user=request.user
            valoration.comment=form.cleaned_data['comment']
            valoration.read_start=form.cleaned_data['read_start']
            valoration.read_end=form.cleaned_data['read_end']
            valoration.save()
            return HttpResponseRedirect(reverse_lazy('valoration-read',args=(valoration.id,)))
    else:
        form = ValorationAddForm()
        form.fields['book'].initial=book
        form.fields['user'].initial=request.user
        form.fields['read_start'].widget.attrs['class'] ='datepicker'
        form.fields['read_end'].widget.attrs['class'] ='datepicker'
    return render(request, 'books/valoration_edit.html', {'form': form})

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('books.add_author',raise_exception=True), name='dispatch')
class AuthorCreate(CreateView):
    model = Author
    fields = ['name', 'family_name', 'birth', 'death', 'gender']
    template_name="books/author_edit.html"

    def get_success_url(self):
        return reverse_lazy('author-read',args=(self.object.id,))

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('books.change_author',raise_exception=True), name='dispatch')
class AuthorUpdate(UpdateView):
    model = Author
    fields = ['name', 'family_name', 'birth', 'death', 'gender']
    template_name="books/author_edit.html"

    def get_success_url(self):
        return reverse_lazy('author-read',args=(self.object.id,))

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('books.delete_author',raise_exception=True), name='dispatch')
class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('home')

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('books.change_book',raise_exception=True), name='dispatch')
class BookUpdate(UpdateView):
    model = Book
    fields = ['title', 'year', 'author']
    template_name="books/book_edit.html"

    def get_success_url(self):
        return reverse_lazy('book-read',args=(self.object.id,))

    def get_form(self, form_class=None): 
        if form_class is None: 
            form_class = self.get_form_class()
        form = super(BookUpdate, self).get_form(form_class)
        form.fields['author'].widget = forms.HiddenInput()
        form.fields['title'].widget.attrs.update({'class': 'big'})
        return form


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('books.delete_book',raise_exception=True), name='dispatch')
class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('home')

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('books.change_valoration',raise_exception=True), name='dispatch')
class ValorationUpdate(UpdateView):
    model = Valoration
    fields = ['book', 'user', 'comment','valoration','read_start','read_end']
    template_name="books/valoration_edit.html"
    success_url = reverse_lazy('valoration-list')

    def get_form(self, form_class=None): 
        if form_class is None: 
            form_class = self.get_form_class()
        form = super(ValorationUpdate, self).get_form(form_class)
        form.fields['book'].widget = forms.HiddenInput()
        form.fields['user'].widget = forms.HiddenInput()
        form.fields['read_start'].widget.attrs['class'] ='datepicker'
        form.fields['read_end'].widget.attrs['class'] ='datepicker'
        return form

    def get_success_url(self):
        return reverse_lazy('valoration-read',args=(self.object.id,))
        
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('books.delete_valoration',raise_exception=True), name='dispatch')
class ValorationDelete(DeleteView):
    model = Valoration
    success_url = reverse_lazy('valoration-list')
    def get_success_url(self):
        return reverse_lazy('book-read',args=(self.object.book.id,))

