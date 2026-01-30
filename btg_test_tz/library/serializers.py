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

class BookCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    author = serializers.CharField()
    publication_year = serializers.IntegerField()
    edition = serializers.IntegerField(required=False, allow_null=True)
    isbn = serializers.CharField()
    total_copies = serializers.IntegerField()

class BookUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    author = serializers.CharField(required=False)
    publication_year = serializers.IntegerField(required=False)
    edition = serializers.IntegerField(required=False, allow_null=True)
    isbn = serializers.CharField(required=False)
    total_copies = serializers.IntegerField(required=False)
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "cpf",
            "email"
        ]

class UserCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()
    cpf = serializers.CharField()

class UserUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    cpf = serializers.CharField(required=False)

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