from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Book, User, Loan
from .serializers import BookSerializer, UserSerializer, LoanSerializer, LoanCreateSerializer
from .services import CreateLoanService, ReturnLoanService

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

class LoanListCreateView(APIView):
    def get(self, request):
        loans = Loan.objects.all()
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = LoanCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(User, id=serializer.validated_data["user_id"])
        book = get_object_or_404(Book, id=serializer.validated_data["book_id"])

        try:
            loan = CreateLoanService().execute(user=user, book=book)
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
        LoanSerializer(loan).data,
        status=status.HTTP_201_CREATED,
        )

class LoanReturnView(APIView):
    def post(self, request, loan_id: int):
        loan = get_object_or_404(Loan, id=loan_id)

        try:
            loan = ReturnLoanService().execute(loan=loan)
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            LoanSerializer(loan).data,
            status=status.HTTP_200_OK,
        )
