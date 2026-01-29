from rest_framework import serializers
from .models import Book, User

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "publication_year",
            "edition",
            "isbn",
            "total_copies"
        ]

        def validate_isbn(self, value):
            if len(value)<10:
                raise serializers.ValidationError("ISBN invalid.")
            return value
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "cpf",
            "email"
        ]