from .domain import LoanDomainService
from .models import Loan
from django.utils import timezone
from .exceptions import BookUnavailable, LoanAlreadyReturned

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
    def execute(self, *, loan: Loan) -> Loan:
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

        return loan