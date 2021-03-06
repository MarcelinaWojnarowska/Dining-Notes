from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('notes', views.notes, name='notes'),
    path('create', views.create_note, name='create_note'),
    path('edit/<int:note_id>', views.edit_note, name='edit_note'),
    path('delete/<int:note_id>', views.delete_note, name='delete_note'),

]

app_name = 'dining_notes'
