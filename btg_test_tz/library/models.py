from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    edition = models.IntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=13, unique=True)
    total_copies = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    cpf = models.CharField(max_length=11, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class Loan(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="loans",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="loans",
    )

    loan_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_active(self) -> bool:
        return self.returned_date is None
    
    def __str__(self) -> str:
        return f"Loan {self.id} - {self.book.title}"