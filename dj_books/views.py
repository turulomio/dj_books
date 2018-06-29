from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.db import transaction
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash,  login
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render,  get_object_or_404,  redirect
from django.contrib.sites.shortcuts import get_current_site

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User

from .tokens import account_activation_token

from books.models import Author,  Book, Valoration
from .forms import UserForm, ProfileForm,  SignUpForm
from books.tables import TableEasyAuthors,  TableEasyValorations, TableEasyBooks

## @todo Add search to search field to repeat search
## @todo Limit search minimum 3 and maximum 50
## @todo Add a tab Widget, author, books, valorations with number in ttab
def home(request):
    search = request.GET.get('search')
    if search!=None:
        searchtitle=_("Looking for '{}' in Library database".format(search))
        books=Book.objects.filter(Q(title__icontains=search) | Q(year__icontains=search))
        authors=Author.objects.filter(Q(name__icontains=search) | Q(family_name__icontains=search))
        if request.user.has_perm('books.search_valoration'):
            valorations=Valoration.objects.filter(comment__icontains=search)
    return render(request, 'home.html', locals())

@login_required
def database(request):
    authors= Author.objects.order_by('name')
    books=Book.objects.order_by('title')
    valorations=Valoration.objects.order_by('read_end')
    tableeasy_authors=TableEasyAuthors(authors)
    tableeasy_books=TableEasyBooks(books)
    tableeasy_valorations=TableEasyValorations(valorations)
    return render(request, 'database.html', locals())

@login_required
def valoration(request):
    valorations= Valoration.objects.order_by('read_start')
    tableeasy_valorations=TableEasyValorations(valorations)
    return render(request, 'valoration.html', locals())
    

## View to register a new user
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = """Hi {},\n\nPlease click on the link below to confirm your registration:\n\nhttp://{}{}""".format(
                    user.username, 
                    current_site.domain, 
                    reverse_lazy(   'activate', 
                                            kwargs={ 'uidb64': urlsafe_base64_encode(force_bytes(user.pk)) , 
                                                            'token': account_activation_token.make_token(user)
                                                          }
                                        )
                    )

            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def account_activation_sent(request):
    return render(request, 'account_activation_sent.html') 
    
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return render(request, 'account_activation_valid.html')
    else:
        return render(request, 'account_activation_invalid.html')

def book_read(request, pk):
    book=get_object_or_404(Book, pk=pk)
    valorations=Valoration.objects.filter(book=book)
    return render(request, 'books/book_read.html', locals())
    
def author_read(request, pk):
    author=get_object_or_404(Author, pk=pk)
    books=Book.objects.filter(author=author)
    return render(request, 'books/author_read.html', locals())


@login_required
@transaction.atomic
def profile_edit(request):
    if request.method == 'POST':

        print(request.POST.dict())
        if "button_profile" in request.POST.dict():
            user_form = UserForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, instance=request.user.profile)
            change_password_form = PasswordChangeForm(request.user)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, _('Your profile was successfully updated!'))

        elif "button_password" in request.POST.dict():
            user_form = UserForm(instance=request.user)
            profile_form = ProfileForm(instance=request.user.profile)
            change_password_form = PasswordChangeForm(request.user, request.POST)
            if change_password_form.is_valid():
                user = change_password_form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, _('Your password was successfully updated!'))

    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        change_password_form = PasswordChangeForm(request.user)
    change_password_form.fields['old_password'].widget.attrs.pop("autofocus", None)
    return render(request, 'profile.html', locals())

## @todo After inserting returns to home. It's ugly

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('books.add_author',raise_exception=True), name='dispatch')
class AuthorCreate(CreateView):
    model = Author
    fields = ['name', 'family_name', 'birth', 'death']
    template_name="books/author_edit.html"

    def get_success_url(self):
        return reverse_lazy('author-read',args=(self.object.id,))

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('books.change_author',raise_exception=True), name='dispatch')
class AuthorUpdate(UpdateView):
    model = Author
    fields = ['name', 'family_name', 'birth', 'death']
    template_name="books/author_edit.html"
    success_url = reverse_lazy('home')

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('books.delete_author',raise_exception=True), name='dispatch')
class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('home')

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('books.add_book',raise_exception=True), name='dispatch')
class BookCreate(CreateView):
    model = Book
    fields = ['title', 'year', 'author']
    template_name="books/book_edit.html"

    def get_success_url(self):
        return reverse_lazy('author-read',args=(self.object.author.id,))

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('books.change_book',raise_exception=True), name='dispatch')
class BookUpdate(UpdateView):
    model = Book
    fields = ['title', 'year', 'author']
    template_name="books/book_edit.html"
    success_url = reverse_lazy('home')


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('books.delete_book',raise_exception=True), name='dispatch')
class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('home')




## @todo user must not be asked
class ValorationCreate(CreateView):
    model = Valoration
    fields = ['book', 'user', 'comment','valoration','read_start','read_end']
    template_name="books/valoration_edit.html"
    success_url = reverse_lazy('valoration-list')

    def get_form(self, form_class=None): 
        if form_class is None: 
            form_class = self.get_form_class()
        form = super(ValorationCreate, self).get_form(form_class)
        form.fields['read_start'].widget.attrs['class'] ='datepicker'
        form.fields['read_end'].widget.attrs['class'] ='datepicker'
        return form

class ValorationUpdate(UpdateView):
    model = Valoration
    fields = ['book', 'user', 'comment','valoration','read_start','read_end']
    template_name="books/valoration_edit.html"
    success_url = reverse_lazy('valoration-list')

    def get_form(self, form_class=None): 
        if form_class is None: 
            form_class = self.get_form_class()
        form = super(ValorationUpdate, self).get_form(form_class)
        form.fields['read_start'].widget.attrs['class'] ='datepicker'
        form.fields['read_end'].widget.attrs['class'] ='datepicker'
        return form

class ValorationDelete(DeleteView):
    model = Valoration
    success_url = reverse_lazy('valoration-list')
