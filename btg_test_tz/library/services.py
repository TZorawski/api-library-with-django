from .domain import LoanDomainService
from .models import Book, User, Loan
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .exceptions import BookUnavailable, LoanAlreadyReturned
from .validations import BookCreateSchema, BookUpdateSchema, UserCreateSchema, UserUpdateSchema

class BookService:
    @staticmethod
    def list_books() -> Book:
        return Book.objects.all()
    
    @staticmethod
    def get_book(book_id: int) -> Book:
        return get_object_or_404(Book, id=book_id)
    
    @staticmethod
    def book_is_available(book_id: int) -> str:
        book = get_object_or_404(Book, id=book_id)
        loans = book.loans.filter(returned_date__isnull=True).count()

        if loans < book.total_copies:
            return "The book is available to loan."

        return "The book is not available to loan."
    
    @staticmethod
    #@transaction.atomic
    def create_book(data: dict) -> Book:
        validated_data = BookCreateSchema(**data)

        book = Book.objects.create(
            title=validated_data.title,
            author=validated_data.author,
            publication_year=validated_data.publication_year,
            edition=validated_data.edition,
            isbn=validated_data.isbn,
            total_copies=validated_data.total_copies,
        )

        return book
    
    @staticmethod
    #@transaction.atomic
    def update_book(book_id: int, data: dict) -> Book:
        book = get_object_or_404(Book, id=book_id)
        validated_data = BookUpdateSchema(**data)

        for field, value in validated_data.model_dump(exclude_unset=True).items():
            setattr(book, field, value)

        book.save()
        return book

class UserService:
    @staticmethod
    def list_users() -> User:
        return User.objects.all()
    
    @staticmethod
    def get_user(user_id: int) -> User:
        return get_object_or_404(User, id=user_id)
    
    @staticmethod
    def list_user_loans(user_id: int) -> Loan:
        return get_object_or_404(User, id=user_id).loans
    
    @staticmethod
    #@transaction.atomic
    def create_user(data: dict) -> User:
        validated_data = UserCreateSchema(**data)

        user = User.objects.create(
            name=validated_data.name,
            email=validated_data.email,
            cpf=validated_data.cpf,
        )

        return user
    
    @staticmethod
    #@transaction.atomic
    def update_user(user_id: int, data: dict) -> Book:
        user = get_object_or_404(User, id=user_id)
        validated_data = UserUpdateSchema(**data)

        for field, value in validated_data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)

        user.save()
        return user

class CreateLoanService:
    def __init__(self):
        self.domain = LoanDomainService()

    #@transaction.atomic
    def execute(self, *, user, book) -> Loan:
        book_active_loans_count = Loan.objects.filter(
            book=book,
            returned_date__isnull=True
        ).count()
        
        if book_active_loans_count >= book.total_copies:
            raise BookUnavailable()
        
        user_active_loans_count = Loan.objects.filter(
            user=user,
            returned_date__isnull=True
        ).count()

        self.domain.validate_user_can_loan(user_active_loans_count)

        due_date = self.domain.calculate_due_date()

        loan = Loan.objects.create(
            user=user,
            book=book,
            due_date=due_date
        )

        return loan

class ReturnLoanService:
    def __init__(self):
        self.domain = LoanDomainService()

    #@transaction.atomic
    def execute(self, *, loan: Loan) -> int:
        if loan.returned_date:
            raise LoanAlreadyReturned()

        returned_date = timezone.now().date()
        fine = self.domain.calculate_fine(
            due_date=loan.due_date,
            returned_date=returned_date
        )

        loan.returned_date = returned_date
        loan.save(update_fields=["returned_date"])

        # Se quiser: persistir multa no futuro
        loan.fine_amount = fine if hasattr(loan, "fine_amount") else None

        return fine