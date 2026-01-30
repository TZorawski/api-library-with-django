from datetime import date
from decimal import Decimal
from django.utils import timezone
from rest_framework import exceptions
from .exceptions import ReachedLimitLoans

class LoanDomainService:
    MAX_ACTIVE_LOANS = 3
    LOAN_DAYS = 14
    DAILY_FINE = Decimal("2.00")

    def validate_user_can_loan(self, user_active_loans_count: int) -> None:
        if user_active_loans_count >= self.MAX_ACTIVE_LOANS:
            raise ReachedLimitLoans()

    def calculate_due_date(self) -> date:
        return timezone.now().date() + timezone.timedelta(days=self.LOAN_DAYS)

    def calculate_fine(self, due_date: date, returned_date: date) -> Decimal:
        if not returned_date:
            return Decimal("0.00")

        returned_date_converted = returned_date

        if returned_date_converted <= due_date:
            return Decimal("0.00")

        days_late = (returned_date_converted - due_date).days
        return days_late * self.DAILY_FINE