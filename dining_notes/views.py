from urllib.parse import urlencode

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date

from .forms import NoteForm, DateForm
from .models import Note

import datetime


def home(request):
    current = datetime.date.today().strftime('%Y-%m-%d')
    return render(request, 'dining_notes/home.html', {'current': current})


def signup_user(request):
    form = UserCreationForm()

    if request.method == 'GET':
        return render(request, 'dining_notes/signupuser.html', {'form': form})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('notes')

            except IntegrityError:
                return render(request, 'dining_notes/signupuser.html', {'form': form,
                                                                        'error': 'That username has already been taken. Pleas choose another username.'})
        else:
            return render(request, 'dining_notes/signupuser.html',
                          {'form': form, 'error': 'Passwords did not match! Try again.'})


def login_user(request):
    form = AuthenticationForm()

    if request.method == 'GET':
        return render(request, 'dining_notes/loginuser.html', {'form': form})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'dining_notes/loginuser.html',
                          {'form': form, 'error': 'Username or password is incorrect'})
        else:
            login(request, user)
            return redirect('notes')


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def notes(request):
    date_from_url = request.GET.get('my_date_field')

    if date_from_url is None:
        date = datetime.date.today()
    else:
        date = parse_date(date_from_url)

    notes = Note.objects.filter(user=request.user, date_added=date).order_by('meal')
    date_form = DateForm()

    return render(request, 'dining_notes/notes.html',
                  {'notes': notes, 'date': date.strftime('%A, %d-%m-%Y'), 'date_form': date_form})


@login_required
def create_note(request):
    form = NoteForm()
    if request.method == 'GET':
        return render(request, 'dining_notes/createnote.html', {'form': form})
    else:
        form = NoteForm(request.POST)
        new_note = form.save(commit=False)
        new_note.user = request.user
        new_note.save()

        base_url = reverse('notes')
        query_string = urlencode({'my_date_field': new_note.date_added})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)


@login_required
def edit_note(request, note_id):
    note = Note.objects.get(id=note_id)
    form = NoteForm(instance=note)
    if request.method == 'GET':
        return render(request, 'dining_notes/editnote.html', {'form': form, 'note': note})
    else:
        form = NoteForm(instance=note, data=request.POST)
        form.save()

        base_url = reverse('notes')
        query_string = urlencode({'my_date_field': note.date_added})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)


@login_required
def delete_note(request, note_id):
    note = Note.objects.get(id=note_id)
    if request.method == 'POST':
        note.delete()

        base_url = reverse('notes')
        query_string = urlencode({'my_date_field': note.date_added})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)
