from flask_login import current_user
from flask import session, redirect, request
from password_validator import PasswordValidator
from markupsafe import escape
from functools import wraps

ALLOWED_EXTENSIONS = {"csv"}

def benefit(value: float) -> str:
    """ Format value as benefit """

    return f"+{currency(value)}"

def benefit_un(un: float) -> str:
    """ Format un as benefit """

    return f"+{un}"

def waste(value: float) -> str:
    """ Format value as waste """

    return f"-{currency(value)}"

def currency(value: float) -> str:
    """Format value as user actual currency."""

    if current_user.user_currency == "Dollars":
        user_currency = "$"
    else:
        user_currency = "€"

    return f"{value:,.2f}{user_currency}"

def currency_filter(user_currency):
    """ HTML currency filter """
    
    return "$" if user_currency == "Dollars" else "€"
 
def percentage(value: float) -> str:
    """ Format value as percentage """

    return f"{value:.2f}%"

def validate_password(password: str) -> bool :
    """  validate password using library 'password_validator' https://pypi.org/project/password-validator/ """

    # Create a schema
    schema = PasswordValidator()

    # Add properties to it
    schema\
    .has().uppercase()\
    .has().lowercase()\
    .has().digits()\
    .has().symbols()\
    .has().no().spaces()\
    
    if schema.validate(password):
        return True
    
    return False

def get_allowed_insert_or_edit_expense_dates(today: object) -> list:
    """ Use date module to get allowed insert or edit expense dates and return a list with dates """

    # Default dates    
    if today.day < 23:
        allowed_dates = [f"{today.month}/{today.year}", f"{today.month + 1}/{today.year}"]
    else:
        allowed_dates = [f"{today.month + 1}/{today.year}", f"{today.month + 2}/{today.year}"]

    # Ensure month is not 11 or 12 
    if today.month == 11 and today.day >= 23 or today.month == 12 and today.day < 23:
        allowed_dates[0] = f"{12}/{today.year}"
        allowed_dates[1] = f"{1}/{today.year + 1}"
    elif today.month == 12 and today.day >= 23:
        allowed_dates[0] = f"{1}/{today.year + 1}"
        allowed_dates[1] = f"{2}/{today.year + 1}"
    
    return allowed_dates

def login_required(f):
    '''Decorate routes to require login. https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/ '''

    @wraps(f)
    def decorated_function(*args, **kwargs):

        # Ensure user is logged
        if current_user.is_anonymous:
            return redirect('/login')
        
        # Allowed routes
        allowed_routes = ["/set_personal_code", "/logout", "/authenticate_login"]

        # Ensure user set personal code and routes that are beeing acessed are not inside allowed routes
        if request.path not in allowed_routes and current_user.personal_code is None:
            return redirect('/set_personal_code')
        
        # Ensure user is authenticated
        try:
            if not session["authenticated"] and request.path not in allowed_routes:
                return redirect('/authenticate_login')
            
        except KeyError:
            if request.path not in allowed_routes:
                return redirect('/authenticate_login')
            
        return f(*args, **kwargs)

    return decorated_function

def clean_form_white_spaces(form_data):
    """ Clean form white spaces and return cleaned data"""

    # Clean keys begin, end and uncessary whitespaces and return cleaned form data
    return {key: " ".join(value.split()) for key,value in form_data.items() if isinstance(value, str)}

def capitalize_string(string):
    """ Split whitespaces and return capitalized strings """

    return " ".join(s.capitalize() for s in string.split())

def has_special_characters(string: str) -> bool:
    """ Check if string has special characters """

    # Escape special characters
    escaped_string = escape(string)

    # Ensure string has special characters
    if string != str(escaped_string) or "'" in string or '"' in string or "`" in string or "`" in string or "%" in string:
        return True
    
    return False

def allowed_file(filename: str) -> str:
    """ https://flask.palletsprojects.com/en/2.3.x/patterns/fileuploads/ """

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_white_spaces(string: str) -> str:
    """ Cleans white spaces from strings and return a clean string with one white space between each word."""

    return " ".join(s for s in string.strip().split()).upper()

def calculate_price_margin(cost_price: float, sell_price: float) -> float:
    """ Calculate product margin """

    return round((((sell_price - cost_price) * 100) / cost_price), 2)

def calculate_total_expenses(expenses: list) -> float:
    """ Calculate expenses total """

    return sum(expense["total"] for expense in expenses)

def set_worker_number(workers: list) -> int:
    """ Set a new registered worker a worker number """
 
    return len(workers) + 100000000

def calculate_regularization_total(actual_stock: int, stock_to_regularize: int , cost_price: float) -> tuple:
    """ Calculate regularization total """

    # Get difference between actual stock and stock to regularize
    stocks_diff = stock_to_regularize - actual_stock

    # Get regularization total
    regularization_total = cost_price * stocks_diff

    if regularization_total < 0:
        regularization_total = str(regularization_total).split("-")[1]
        
    # Return regularization total
    return (float(regularization_total), stocks_diff)

def calculate_waste_total(stock_to_waste: int, cost_price: float) -> float:
    """ Calculate waste total """

    # Return waste total converted to waste
    return cost_price * float(stock_to_waste)