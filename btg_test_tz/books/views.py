from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import status
from .models import Book
from .serializers import BookSerializer

@api_view(['GET'])
def index(request):
    return HttpResponse("Heloo user")

@api_view(['POST'])
def create(request):
    serializer = BookSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get(request, id):
    book = get_object_or_404(Book, id=id)
    serializer = BookSerializer(book)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_all(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def put(request, id):
    book = get_object_or_404(Book, id=id)
    serializer = BookSerializer(book, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()

    return Response({"detail: Book successfully deleted"}, status=status.HTTP_204_NO_CONTENT)