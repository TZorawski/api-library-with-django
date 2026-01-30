def format_pydantic_errors(e):
    errors_formatted = {}
    for error in e.errors():
        field = error['loc'][0]
        errors_formatted[field] = [error['msg']]
        
    return errors_formatted