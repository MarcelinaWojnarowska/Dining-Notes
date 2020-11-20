from urllib.parse import urlencode

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from django.utils.timezone import now

from .forms import NoteForm, DateForm
from .models import Note


def home(request):
    return render(request, 'dining_notes/home.html')


@login_required
def notes(request):
    date_from_url = request.GET.get('my_date_field')

    if date_from_url is None:
        date = now()
    else:
        date = parse_date(date_from_url)

    my_notes = Note.objects.filter(user=request.user, date_added=date).order_by('meal')
    date_form = DateForm()

    return render(request, 'dining_notes/notes.html',
                  {'notes': my_notes, 'date': date.strftime('%A, %d-%m-%Y'), 'date_form': date_form})


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

        base_url = reverse('dining_notes:notes')
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

        base_url = reverse('dining_notes:notes')
        query_string = urlencode({'my_date_field': note.date_added})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)


@login_required
def delete_note(request, note_id):
    note = Note.objects.get(id=note_id)
    if request.method == 'POST':
        note.delete()

        base_url = reverse('dining_notes:notes')
        query_string = urlencode({'my_date_field': note.date_added})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)
