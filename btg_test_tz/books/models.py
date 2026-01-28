from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    edition = models.IntegerField()
    isbn = models.CharField(max_length=13, unique=True)
    total_copies = models.IntegerField()

    #def __str__(self) -> str:
    #    return self.title

