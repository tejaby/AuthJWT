from rest_framework import serializers

from apps.user.api.serializers import UserListSerializer

from apps.note.models import Note


class NoteSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = Note
        fields = '__all__'
