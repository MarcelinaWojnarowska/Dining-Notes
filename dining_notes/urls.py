from django.urls import path
from . import views

urlpatterns = [
    # Dining notes
    path('', views.home, name='home'),
    path('notes/', views.notes, name='notes'),
    path('create/', views.create_note, name='create_note'),
    path('edit/<int:note_id>', views.edit_note, name='edit_note'),
    path('delete/<int:note_id>', views.delete_note, name='delete_note'),

    # Auth
    path('signup/', views.signup_user, name='signup_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),

]
