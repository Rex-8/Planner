from django.urls import path,include
from . import views

app_name = 'Content'

urlpatterns = [
    path('',views.home,name='home'),
    path('favs/',views.favs,name='favs'),
    path('notes/',views.notes,name='notes'),
    path('todolists/',views.todolists,name='todolists'),
    path('view/<slug:slug>',views.view_content,name='content_page'),
    path('create/', views.create_content, name='create_content'),
    path('create/note',views.create_note,name='create_note'),
    path('create/todolist',views.create_todolist,name='create_todolist'),
]
