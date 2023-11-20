from django.urls import path

from apps.note.api.api import NoteListAPIView

urlpatterns = [
    path('note/', NoteListAPIView.as_view(), name='note'),
]
