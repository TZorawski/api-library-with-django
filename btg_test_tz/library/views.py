from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Book, User, Loan
from .serializers import BookSerializer, BookCreateSerializer, BookUpdateSerializer, UserSerializer, UserCreateSerializer, UserUpdateSerializer, LoanSerializer, LoanCreateSerializer
from .services import BookService, UserService, CreateLoanService, ReturnLoanService
from pydantic import ValidationError

def format_pydantic_errors(e):
    errors_formatted = {}
    for error in e.errors():
        field = error['loc'][0]
        errors_formatted[field] = [error['msg']]
        
    return errors_formatted

class BookListCreateView(APIView):
    def get(self, request):
        books = BookService.list_books()
        return Response(BookSerializer(books, many=True).data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = BookCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            book = BookService.create_book(serializer.validated_data)
        except ValidationError as e:
            errors_formatted = format_pydantic_errors(e)
            return Response(
                errors_formatted,
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            BookSerializer(book).data,
            status=status.HTTP_201_CREATED,
        )
    
class BookEditDetailView(APIView):
    def get(self, request, id: int):
        book = BookService.get_book(book_id=id)
        return Response(BookSerializer(book).data, status=status.HTTP_200_OK)

    #def put(self, request, id: int):
    #    serializer = BookUpdateSerializer(data=request.data, partial=True)
    #    serializer.is_valid(raise_exception=True)
    #
    #    if serializer.is_valid():
    #        serializer.save()
    #        return Response(serializer.data, status=status.HTTP_200_OK)
    #
    #    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, id: int):
        serializer = BookUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            book = BookService.update_book(
                book_id=id,
                data=serializer.validated_data,
            )
        except ValidationError as e:
            errors_formatted = format_pydantic_errors(e)
            return Response(
                errors_formatted,
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            BookSerializer(book).data,
            status=status.HTTP_200_OK,
        )
    
    #def delete(self, request, id):
    #    book = get_object_or_404(Book, id=id)
    #    book.delete()
    #    return Response({"detail: Book successfully deleted"}, status=status.HTTP_204_NO_CONTENT)

class BookAvailabilityView(APIView):
    def get(self, request, id):
        is_available = BookService.book_is_available(book_id=id)

        return Response(is_available, status=status.HTTP_200_OK)

class UserListCreateView(APIView):
    def get(self, request):
        users = UserService.list_users()
        return Response(UserSerializer(users, many=True).data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = UserService.create_user(serializer.validated_data)
        except ValidationError as e:
            errors_formatted = format_pydantic_errors(e)
            return Response(
                errors_formatted,
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )
    
class UserEditDetailView(APIView):
    def get(self, request, id: int):
        user = UserService.get_user(user_id=id)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    #def put(self, request, id):
    #    user = get_object_or_404(User, id=id)
    #    serializer = UserSerializer(user, data=request.data)
    #
    #    if serializer.is_valid():
    #        serializer.save()
    #        return Response(serializer.data, status=status.HTTP_200_OK)
    #
    #    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, id):
        serializer = UserUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            user = UserService.update_user(
                user_id=id,
                data=serializer.validated_data,
            )
        except ValidationError as e:
            errors_formatted = format_pydantic_errors(e)
            return Response(
                errors_formatted,
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_200_OK,
        )
    
    #def delete(self, request, id):
    #    user = get_object_or_404(User, id=id)
    #    user.delete()
    #    return Response({"detail: User successfully deleted"}, status=status.HTTP_204_NO_CONTENT)

class UserLoansListView(APIView):
    def get(self, request, id):
        loans = UserService.list_user_loans(user_id=id)
        return Response(LoanSerializer(loans, many=True).data, status=status.HTTP_200_OK)

class LoanListCreateView(APIView):
    def get(self, request):
        loans = Loan.objects.all()
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = LoanCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(User, id=serializer.validated_data["user_id"])
        book = get_object_or_404(Book, id=serializer.validated_data["book_id"])

        try:
            loan = CreateLoanService().execute(user=user, book=book)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(LoanSerializer(loan).data, status=status.HTTP_201_CREATED)
    
class LoanActivetedList(APIView):
    def get(self, request):
        loans = Loan.objects.filter(returned_date__isnull=True)
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LoanReturnView(APIView):
    def post(self, request, loan_id: int):
        loan = get_object_or_404(Loan, id=loan_id)
        fine = 0.0

        try:
            fine = ReturnLoanService().execute(loan=loan)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"fine": fine}, status=status.HTTP_200_OK)

class LoanListByUserView(APIView):
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        loans = Loan.objects.filter(user=user)
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)