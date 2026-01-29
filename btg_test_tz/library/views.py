from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Book, User
from .serializers import BookSerializer, UserSerializer

class BookListCreateView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BookEditDetailView(APIView):
    def get(self, request, id):
        book = get_object_or_404(Book, id=id)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        book = get_object_or_404(Book, id=id)
        serializer = BookSerializer(book, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, id):
        book = get_object_or_404(Book, id=id)
        serializer = BookSerializer(book, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #def delete(self, request, id):
    #    book = get_object_or_404(Book, id=id)
    #    book.delete()
    #    return Response({"detail: Book successfully deleted"}, status=status.HTTP_204_NO_CONTENT)

class UserListCreateView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserEditDetailView(APIView):
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        user = get_object_or_404(User, id=id)
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, id):
        user = get_object_or_404(User, id=id)
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #def delete(self, request, id):
    #    user = get_object_or_404(User, id=id)
    #    user.delete()
    #    return Response({"detail: User successfully deleted"}, status=status.HTTP_204_NO_CONTENT)