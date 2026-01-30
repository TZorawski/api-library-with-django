from rest_framework.exceptions import APIException

class ISBNAlredyExists(APIException):
    status_code = 400
    default_detail = "The ISBN already exists in the database."
    default_code = "isbn_alredy_exists"

class CPFAlredyExists(APIException):
    status_code = 400
    default_detail = "The CPF already exists in the database."
    default_code = "cpf_alredy_exists"

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