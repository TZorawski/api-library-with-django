from rest_framework import serializers
from .models import Book, User, Loan

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

class LoanSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = Loan
        fields = [
            "id",
            "user",
            "book",
            "loan_date",
            "due_date",
            "returned_date",
            "is_active"
        ]

class LoanCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    book_id = serializers.IntegerField()