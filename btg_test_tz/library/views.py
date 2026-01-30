from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookSerializer, BookCreateSerializer, BookUpdateSerializer, UserSerializer, UserCreateSerializer, UserUpdateSerializer, LoanSerializer, LoanCreateSerializer
from .services import BookService, UserService, LoanService
from pydantic import ValidationError
from .utils import format_pydantic_errors

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

class UserLoansListView(APIView):
    def get(self, request, id):
        loans = UserService.list_user_loans(user_id=id)
        return Response(LoanSerializer(loans, many=True).data, status=status.HTTP_200_OK)

class LoanListCreateView(APIView):
    def get(self, request):
        loans = LoanService.list_loans()
        return Response(LoanSerializer(loans, many=True).data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = LoanCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            loan = LoanService.create_loan(serializer.validated_data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            errors_formatted = format_pydantic_errors(e)
            return Response(
                errors_formatted,
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(LoanSerializer(loan).data, status=status.HTTP_201_CREATED)
    
class LoanActivetedList(APIView):
    def get(self, request):
        loans = LoanService.list_actives_loans()
        return Response(LoanSerializer(loans, many=True).data, status=status.HTTP_200_OK)

class LoanReturnView(APIView):
    def patch(self, request, id: int):
        fine = 0.0

        try:
            fine = LoanService.return_loan(loan_id=id)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"fine": fine}, status=status.HTTP_200_OK)

class LoanListByUserView(APIView):
    def get(self, request, id):
        loans = LoanService.list_loans_by_user(user_id=id)
        return Response(LoanSerializer(loans, many=True).data, status=status.HTTP_200_OK)