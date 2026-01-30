from rest_framework.exceptions import APIException

class ReachedLimitLoans(APIException):
    status_code = 400
    default_detail = "User has reached the maximum limit for active loans."
    default_code = "reached_limit_loans"

class BookUnavailable(APIException):
    status_code = 400
    default_detail = "Book unavailable for loan."
    default_code = "book_unavailable"

class LoanAlreadyReturned(APIException):
    status_code = 400
    default_detail = "The loan has already been returned."
    default_code = "loan_already_returned"