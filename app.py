from flask import Flask, flash, jsonify, redirect, render_template, request, session, abort, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from markupsafe import escape
from werkzeug.utils import safe_join
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer
from form_models import *
from cs50 import SQL
from flask_session import Session
from helpers import *
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from io import StringIO
from db_helper import DataBaseHelper
from sqlalchemy import create_engine

import math
import json
import csv
import os

__all__ = [
    "currency",
    "percentage",
    "benefit",
    "benefit_un",
    "currency_filter",
    "login_required",
    "calculate_price_margin",
    "capitalize_string",
    "set_worker_number",
    "get_allowed_insert_or_edit_expense_dates",
    "calculate_total_expenses",
    "has_special_characters",
    "clean_form_white_spaces",
    "registerUserForm",
    "loginUserForm",
    "personalCodeForm",
    "recoverPasswordForm",
    "defineNewPasswordForm",
    "registerProductInOrderForm",
    "registerExpenseForm",
    "registerWasteForm",
    "registerRegularizationForm",
    "registerProductForm",
    "registerServiceForm",
    "registerWorkerForm",
    "registerAbsenceForm",
    "consultAbsencesForm",
    "registerBenefitForm",
    "consultBenefitsForm",
    "searchProductsAndServicesForm",
    "searchAndEditForm",
    "checkExpensesForm",
    "createInventoryForm",
    "changeCompanyNameForm",
    "changeCurrencyForm",
    "authenticatePasswordForm",
    "authenticatePersonalCodeForm"
    ]

# Configure application
app = Flask(__name__)

# Custom filters
app.jinja_env.filters["currency"] = currency
app.jinja_env.filters["percentage"] = percentage
app.jinja_env.filters["benefit"] = benefit
app.jinja_env.filters["benefit_un"] = benefit_un
app.jinja_env.filters["currency_filter"] = currency_filter

# Configure upload size limit
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Configure download folder
FILES_DIRECTORY = 'downloads/'

# Configure to allow specific extensions for security
ALLOWED_EXTENSIONS = {"csv"}

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Configure app SECRET KEY
app.config['SECRET_KEY'] = os.urandom(24)

# Configure session to set tokens a duration time
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)

# Configure flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///smallbiz_project.db")
pos_db = SQL("sqlite:///pos_sales.db")

# Configure db and pos_db to clean queue pool after 3600 miliseconds and set max_overflow to 0
# https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine
_ = create_engine("sqlite:///smallbiz_project.db", pool_recycle=3600, max_overflow=0)
_ = create_engine("sqlite:///pos_sales.db", pool_recycle=3600, max_overflow=0)

# Initiate app
Session(app)

# Unity measures for products
UNITY_MEASUREMENT = ["UN", "KG"]

# Product Families
CATEGORIES = [
            {"id": 1001, "category": "Grocery", "sub_categories": [
                     {"sub_category_id": 10011, "sub_category": "Pantry staples"},
                     {"sub_category_id": 10012, "sub_category": "Snacks"},
                     {"sub_category_id": 10013, "sub_category": "Canned goods"},
                     {"sub_category_id": 10014, "sub_category": "Dry goods"}]
                     },
            {"id": 1002, "category": "Drinks", "sub_categories": [
                     {"sub_category_id": 10021, "sub_category": "Waters"},
                     {"sub_category_id": 10022, "sub_category": "Sodas"},
                     {"sub_category_id": 10023, "sub_category": "Fruit juices"},
                     {"sub_category_id": 10024, "sub_category": "Wines"},
                     {"sub_category_id": 10025, "sub_category": "Beers"},
                     {"sub_category_id": 10026, "sub_category": "Spirits"}]
                     },
            {"id": 1003, "category":  "Chandlery", "sub_categories": [
                     {"sub_category_id": 10031, "sub_category": "Pharmacy"},
                     {"sub_category_id": 10032, "sub_category": "Health and beauty"},
                     {"sub_category_id": 10033, "sub_category": "Household essentials"}]
                     },
            {"id": 1004, "category": "Fruits and Vegetables", "sub_categories": [
                     {"sub_category_id": 10041, "sub_category": "Fruits"},
                     {"sub_category_id": 10042, "sub_category": "Vegetables"}]
                     },
            {"id": 1005, "category": "Butcher", "sub_categories": [
                     {"sub_category_id": 10051, "sub_category": "Poultry"},
                     {"sub_category_id": 10052, "sub_category": "Beef"},
                     {"sub_category_id": 10053, "sub_category": "Pork"}]
                     },
            {"id": 1006, "category": "Sea food", "sub_categories": [
                     {"sub_category_id": 10061, "sub_category": "Fresh fish"},
                     {"sub_category_id": 10062, "sub_category": "Frozen fish"},
                     {"sub_category_id": 10063, "sub_category": "Shellfish"}]
                    },
            {"id": 1007, "category": "Charcuterie", "sub_categories": [
                     {"sub_category_id": 10071, "sub_category": "Cold cuts"},
                     {"sub_category_id": 10072, "sub_category": "Chesses"},
                     {"sub_category_id": 10073, "sub_category": "Prepared foods"},
                     {"sub_category_id": 10074, "sub_category": "Sausages"}]
                     },
            {"id": 1008, "category": "Dairy", "sub_categories": [
                     {"sub_category_id": 10081, "sub_category": "Milk"},
                     {"sub_category_id": 10082, "sub_category": "Yogurts"},
                     {"sub_category_id": 10083, "sub_category": "Cheeses"},
                     {"sub_category_id": 10084, "sub_category": "Egs"}]
            }]

# Expenses
EXPENSE_TYPES = [
    {"expense_id": 301, "expense_description": "Water, electricity and fuel"}, 
    {"expense_id": 302, "expense_description": "Office supplies"},
    {"expense_id": 303, "expense_description": "Comunications"},
    {"expense_id": 304, "expense_description": "Maintenaince and repair"},
    {"expense_id": 305, "expense_description": "Cleaning, security and transports"},
    {"expense_id": 306, "expense_description": "Insurance"},
    {"expense_id": 307, "expense_description": "Advertising"},
    {"expense_id": 308, "expense_description":  "Rent"}]

# Sections
SECTIONS = ["Management", 
            "Store workers", 
            "Butcher", 
            "Fishmonger", 
            "Bakery", 
            "Fruits and Vegetables"]

# Movements
MOVEMENTS = [{"movement_id": 101, "movement_description": "Order entry"},
            {"movement_id": 102, "movement_description": "Regularization waste"}, 
            {"movement_id": 103, "movement_description": "Regularization benefit"}, 
            {"movement_id": 104, "movement_description": "Identified waste"},
            {"movement_id": 105, "movement_description": "Inventory waste"},
            {"movement_id": 106, "movement_description": "Inventory benefit"},
            {"movement_id": 107, "movement_description": "Sale"},
            {"movement_id": 108, "movement_description": "Refund sale"},
            {"movement_id": 109, "movement_description": "Register entry"}]

# Waste motives
WASTE_MOTIVES = [{"waste_id": 201, "waste_description": "Expired"},
                 {"waste_id": 202, "waste_description": "Damaged"},
                 {"waste_id": 203, "waste_description": "Transport failure"}]

# Configure user class from Flask-login

class User(UserMixin):
    """ https://flask-login.readthedocs.io/en/latest/ """

    def __init__(self, user_id, email, password, user_currency, personal_code, company_name, db_connection):
        self.id = user_id
        self.email = email
        self.password = password
        self.user_currency = user_currency
        self.personal_code = personal_code
        self.company_name = company_name
        self.db_connection = db_connection

    @classmethod
    def get(cls, email):

        db_connection = DataBaseHelper(db, email=email)

        user = db_connection.get_user()

        # If user exists return user information, else return None
        if user:
            # Get user information
            user = user[0]

            # Get company user info
            company_info = db_connection.query_company()

            return cls(user_id=user["id"], email=user["email"], password=user["hash"], user_currency=company_info[0]["currency"], personal_code=user["personal_code"], company_name=company_info[0]["name"], db_connection=db_connection)

        return None

@login_manager.user_loader
def load_user(user_id):
    # Query user
    print("load")
    
    db_connection = DataBaseHelper(db, user_id=user_id)

    # Get user
    user = db_connection.get_user()

    # If user exists return user information, else return None
    if user: 
        # Get user information
        user = user[0]

        # Get company user info
        company_info = db_connection.query_company()

        return User(user_id=user["id"], email=user["email"], password=user["hash"], user_currency=company_info[0]["currency"],  personal_code=user["personal_code"], company_name=company_info[0]["name"], db_connection=db_connection)

    # Load user database
    return User.get(user_id)

@app.after_request
def after_request(response):
    """ Ensure responses aren't cached and configure CSP """
    
    # Configure Content-Security-Policy to ensure all app scripts, images and sources are provided by server-side
    # Had some troubles to understand when I was working in security of app. Searched some foruns but i was having some errors so I consulted ChatGPT
    # to understand and help me in this case 
    response.headers['Content-Security-Policy'] = ( 
                        "default-src 'self'; "
                        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.8.3/font/bootstrap-icons.min.css; "
                        "script-src 'self' https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js https://cdn.jsdelivr.net/npm/chart.js;"
                        "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
                        "img-src 'self' data:;"
    )

    # Ensure responses aren't chached
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    return response

@app.errorhandler(400)
def bad_request(error):
    """ Custom error handler for 400 Bad Request """
    # https://flask.palletsprojects.com/en/latest/quickstart/#redirects-and-errors

    response = jsonify({"error": str(error.description)})
    return response, 400

@app.errorhandler(500)
def internal_error(error):
    """ Custom error handler for 500 Internal Server Error """
    # https://flask.palletsprojects.com/en/latest/quickstart/#redirects-and-errors

    response = jsonify({"error": str(error.description)})
    return response, 500

@app.route('/download/<filename>')
@login_required
def download_file(filename):
    """ Route to download files """
    try:
        # Use safe_join to prevent directory traversal attacks
        _ = safe_join(FILES_DIRECTORY, filename)

        # Return file to user
        return send_from_directory(FILES_DIRECTORY, filename, as_attachment=True)
    
    except FileNotFoundError:
        abort(404, description="File not found!")

@app.route("/")
def index():
    """ inital page """

    # Ensure user is logged in
    if current_user.is_authenticated:
        # Ensure user has personal code set
        if not current_user.personal_code:
            return redirect("/set_personal_code")
        
        # Ensure user already authenticated login
        try:
            if not session["authenticated"]:
                return redirect("/authenticate_login")
        except KeyError:
            return redirect("/authenticate_login")

    # User reached via GET
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register user """

    # Create Flask-WTF register user form
    form = registerUserForm()

    # User reached by POST
    if form.validate_on_submit():
        # Get email
        email = form.email.data

        # Get user password
        password = form.password.data

        # Get user company name
        company_name = form.company_name.data

        # Get user currency
        user_currency = form.currency.data

        # Convert email to lowercase
        email = email.lower()

        try:
            # Begin databases transactions
            db.execute("BEGIN TRANSACTION")
            pos_db.execute("BEGIN TRANSACTION")

            try:
                # Insert user in users in to database
                db.execute("INSERT INTO users (email, hash) VALUES (?,?)", email, generate_password_hash(password))
            except (ValueError, RuntimeError, TypeError, AttributeError, KeyError):
                # Flash user with error
                flash("Email already registered!", "danger")

                # Return register.html rendered
                return render_template("/register.html", form=form)

            # Get user id
            user_id = db.execute("SELECT id FROM users WHERE email = ?", email)
            user_id = user_id[0]["id"]

            # Inser company in companies
            db.execute("INSERT INTO companies (name, currency, user_id) VALUES(?,?,?)", company_name, user_currency, user_id)

            # Insert user
            pos_db.execute("INSERT INTO pos_system(user_id) VALUES(?)", user_id)

            # Commit transactions
            db.execute("COMMIT")
            pos_db.execute("COMMIT")

        except (ValueError, RuntimeError, TypeError, AttributeError, KeyError):

            # Rollback transactions
            db.execute("ROLLBACK")
            pos_db.execute("ROLLBACK")

            # Flash user with error message
            flash("Something wen't wrong! Try again!", "danger")  

            # Redirect user to same template with error message
            return render_template("register.html", form=form)

        # Flash user
        flash("Registered with success!", "success")

        # Redirect user to login page
        return redirect("/login")
    
    # User reached via GET
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """ Log user in"""

    form = loginUserForm()

    # Ensure login form is validated
    if form.validate_on_submit():
        
        # Get user validation
        user = User.get(form.email.data)

        # Get password in form
        password = form.password.data

        # Ensure user exists and password is valid
        if user and check_password_hash(user.password, password):
            # Ensure user wants to remember session
            if form.remember.data:
                # Login user and save a remember session cookie with duration of 7 days
                login_user(user, remember=True)
            else:
                # Login user
                login_user(user)
    
            # Redirect user to index
            return redirect("/")
        
        else:
            # Flash user with error message
            flash("Invalid email or password.", "danger")

    # User reached via GET        
    return render_template("login.html", form=form)

@app.route("/authenticate_login", methods=["GET", "POST"])
@login_required
def authenticate_login():
    """ Render authenticate_login.html """

    # Create Flask-WTF authenticate personal code form 
    form = authenticatePersonalCodeForm()

    if form.validate_on_submit():
        # Query user personal code
        if check_password_hash(current_user.personal_code, form.personal_code.data):
            # Flash user with success message
            flash("Authenticated with success.", "success")

            # Set session to authenticated
            session["authenticated"] = True

            # Redirect user to index
            return redirect("/")
        else:
            # Flash user with invalid personal code message
            flash("Invalid personal code.", "danger")

            # Redirect user to authenticate login again
            return redirect("/authenticate_login")

    return render_template("/authenticate_login.html", form=form)

@app.route("/set_personal_code", methods=["GET", "POST"])
@login_required
def set_personal_code():
    """ Set personal code and set user to active """

    # Ensure user has already set personal code
    if current_user.personal_code:
        redirect("/")

    # Create Flask-WTF personal code form 
    form = personalCodeForm()

    # Ensure form data is valid
    if form.validate_on_submit():
        # Insert personal code in db
        current_user.db_connection.insert_personal_code(generate_password_hash(form.personal_code.data))

        flash("Personal code set with success.", "success")

        return redirect("/")

    # User reached via GET
    return render_template("set_personal_code.html", form=form)

@app.route("/recover_password", methods=["GET", "POST"])
def recover_password():
    """ Recover password """

    # Get recover password form
    form = recoverPasswordForm()

    # Ensure recover form is validated
    if form.validate_on_submit():
        # Ensure email inserted is associated with personal code
        user = User.get(form.email.data)

        if not user:
            flash("Invalid credentials!", "danger")
            return redirect("/recover_password")
        else:
            # Query user personal code
            user_personal_code = db.execute("SELECT personal_code FROM users WHERE email = ?", form.email.data)

            # Ensure personal code is valid
            if not user.personal_code:
                flash("Looks like has a problema to recover your password. Email smallbiz@randomemail.com with subject 'Recover password'!")
            else:
                if not check_password_hash(user_personal_code[0]["personal_code"], form.personal_code.data):
                    # Flash user with error
                    flash("Invalid credentials!", "danger")

                    # Redirect user to same url
                    return redirect("/recover_password")
                else:
                    # Flash user
                    flash("Credentials validated with success! Define your new password.", "success")

                    # Serialize secret key
                    s = Serializer(app.config["SECRET_KEY"]) # https://itsdangerous.palletsprojects.com/en/stable/url_safe/

                    # Create a token with user email
                    email_token = s.dumps({'email': form.email.data})

                    # Redirect user to define new password
                    return redirect(f"/define_new_password/{email_token}")

    return render_template("recover_password.html", form=form)

@app.route("/define_new_password/<email_token>", methods=["GET", "POST"])
def define_new_password(email_token=None):
    """ Define new password """

    # Get define new password form
    form = defineNewPasswordForm()

    try:
        # Read email token
        data = Serializer(app.config["SECRET_KEY"]).loads(email_token, max_age=3600) # https://itsdangerous.palletsprojects.com/en/stable/url_safe/
    
    except (ValueError, RuntimeError, TypeError, AttributeError, KeyError):

        # Flash user with error message
        flash("Time expired! Try again!", "danger")
            
        # Redirect user to recover password again 
        return redirect("/recover_password")

    if form.validate_on_submit():
        # Update user password
        db.execute("UPDATE users SET hash = ? WHERE email = ?", generate_password_hash(form.new_password.data), data["email"])

        # Flash user with success message
        flash("New password defined with success!", "success")

        # Redirect user to login
        return redirect("/login")
    
    # Render define_new_password.html with form and email token
    return render_template("define_new_password.html", form=form, email_token=email_token)

@app.route("/settings")
@login_required
def settings():
    """ Render user settings """

    return render_template("settings.html")

@app.route("/logout")
@login_required
def logout():
    """ log out user """
    
    # Forget any user id
    logout_user()

    # Clear session
    session.clear()

    # Return user to index 
    return redirect("/login")

@app.route("/delete_account")
@login_required
def delete_account():
    """" Delete user account """

    # Delete user from database
    db.execute("DELETE FROM users WHERE id = ?", current_user.id)
    pos_db.execute("DELETE FROM pos_system WHERE user_id = ?", current_user.id)

    # Clear session
    session.clear()

    # Logout user
    logout_user()

    flash("Account deleted with success! Hope to see you soon again!", "success")

    return redirect("/")

@app.route("/open_store", methods=["POST"])
def open_store():
    """ Update session store status to open """

    # Query user products
    if not current_user.db_connection.query_all_products():
        abort(400, description="Register products to use <span class='personal-blue-color'>POS</div>!")

    try:
        # Get store status
        store_status = session["store_status"]

        # Ensure store is closed or closed and monitoring
        if store_status == "closed":
            # Set session store status to open
            session["store_status"] = "open"

            # Set session datetime open store
            session["store_open_datetime"] = datetime.now()
        else:
            # Set session store status to monitoring
            session["store_status"] = "monitoring"

    except KeyError:
        # Set session store status to open
        session["store_status"] = "open"
        
        # Set session datetime open store
        session["store_open_datetime"] = datetime.now()

    # Return layour.html updated as response
    return jsonify({"sucess_message": "Store open!"})

@app.route("/close_store", methods=["POST"])
def close_store():
    """ Update session store status to closed"""
    
    # Set session store status to open
    session["store_status"] = "closed"

    # Set session store close datetime
    session["store_close_datetime"] = datetime.now()
    
    # Get sales from open store datetime till now
    sales_info = pos_db.execute("SELECT IFNULL(SUM(total),0) AS sales, COUNT(id) AS clients from pos_sales_records WHERE datetime BETWEEN ? AND ? AND pos_id = (SELECT id FROM pos_system WHERE user_id = ?)", session["store_open_datetime"], datetime.now(), current_user.id)
    
    sales = sales_info[0]["sales"]
    clients = sales_info[0]["clients"]

    try:
        median_sale_for_client = round(sales / float(clients), 2)
    except ZeroDivisionError:
        median_sale_for_client = 0

    sales_report_html = f"""
                        <div class="col-lg-12 mt-3 mb-3">
                            <div class="row text-center mx-auto">
                                <div class="col-lg-6 mt-2">
                                    <div class="col-lg-12 border rounded-2 p-2 shadow">
                                        <div class="col-lg-12 mb-2">Sales</div>
                                        <div class="col-lg-12 mt-2 mb-2 personal-blue-color f-bold"><h5>{currency(sales)}</h5></div>
                                    </div>
                                </div>
                                <div class="col-lg-6 mt-2">
                                    <div class="col-lg-12 border rounded-2 p-2 shadow">
                                        <div class="col-lg-12 mb-2">Clients</div>
                                        <div class="col-lg-12 mt-2 mb-2 personal-blue-color f-bold"><h5>{clients}</h5></div>
                                    </div>
                                </div>
                                <div class="col-lg-6 mt-2">
                                    <div class="col-lg-12 border rounded-2 p-2 shadow">
                                        <div class="col-lg-12 mb-2">Median sale(€)/client</div>
                                        <div class="col-lg-12 mt-2 mb-2 personal-blue-color f-bold"><h5>{currency(median_sale_for_client)}</h5></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        """

    # Return layour.html updated as response
    return jsonify({"sales_report_html": sales_report_html})

@app.route("/start_monitoring", methods=["POST"])
def start_monitoring_sales_and_clients():
    """ Update session store status to monitoring """

    # Set session store status to open
    session["store_status"] = "monitoring"

    # Return layour.html updated as response
    return jsonify({"sucess_message": "Monitoring!"})

@app.route("/stop_monitoring", methods=["POST"])
def stop_monitoring_sales_and_clients():
    """ Update session store status to monitoring """

    # Set session store status to open
    session["store_status"] = "open"

    # Return layour.html updated as response
    return jsonify({"sucess_message": "Monitoring!"})

@app.route("/pos", methods=["POST"])
def pos():
    """ Render pos.html and return template as response """

    # Bar code reader mode
    bar_code_reader_mode = request.data.decode("utf-8")

    if bar_code_reader_mode == "manual_mode":
        session["store_status"] = "pos_manual_mode"
    else:
        session["store_status"] = "pos_scan_mode"

    purchase_total = 0

    # Check if a purchase is active
    try:
        # Get active purchase
        purchase_info = session["purchase"]

        # Get purchase total
        for registry in purchase_info:
            purchase_total += registry["registry_total"]   

    except KeyError:
        purchase_info = []

    print(session["store_status"])

    # Render pos_purchase_info.html
    pos_purchase_info = render_template("pos_templates/pos_purchase_info.html", purchase_info=purchase_info, purchase_total=purchase_total)
    
    return jsonify({"pos_html": render_template("pos_templates/pos.html", pos_purchase_info=pos_purchase_info)})

@app.route("/start_pos", methods=["POST"])
def start_pos():
    """ Render start_pos.html and return template as response """

    return jsonify({"start_pos_html": render_template("pos_templates/start_pos.html")})

@app.route("/send_pos_purchase_info_rendered")
def pos_purchase_info_rendered():
    """ Render pos_purchase_info.html and return as response """

    purchase_total = 0

    # Check if a purchase is active
    try:
        # Get active purchase
        purchase_info = session["purchase"]

        # Get purchase total
        for registry in purchase_info:
            purchase_total += registry["registry_total"]   

    except KeyError:
        purchase_info = []

    return jsonify({"pos_purchase_info_html": render_template("pos_templates/pos_purchase_info.html", purchase_info=purchase_info, purchase_total=purchase_total)})

@app.route("/delete_pos_registry", methods=["POST"])
def pos_delete_registry():
    """ Delete  pos registry """

    # Purchase Index
    purchase_index = request.data.decode("utf-8") 

    purchase_info = session["purchase"]

    del purchase_info[int(purchase_index)]

    session["purchase"] = purchase_info

    return jsonify({"message": "Registry deleted with sucess!"})

@app.route('/copy_pos_last_registry')
def pos_copy_pos_last_registry():
    """ Copy pos last registry and update session["purchase"] """

    # Get last pos registry
    last_pos_registry = session["purchase"][-1]

    # Append to session purchase information last pos registry
    session["purchase"].append(last_pos_registry)

    return jsonify({"message": "Last registry copied with success!"})

@app.route('/refund_selected_products', methods=["POST"])
def pos_refund_selected_products():
    """ Refund selected products from sale """

    # Refund sale data
    refund_sale_data = request.get_json()

    # Get products id and units to refund
    products_services_data = refund_sale_data["ids_and_units"]

    print(products_services_data)

    # Sale id
    sale_id = refund_sale_data["sale_id"]

    # Escape special characters
    sale_id = escape(sale_id)

    # Request pos sale record data
    pos_recorded_data = pos_db.execute("SELECT * FROM pos_sales_records WHERE id = ?", sale_id)

    # Ensure sale exist
    if not pos_recorded_data:
        abort(400, description="Sale doesn't exist!")
    
    # Get sales data
    recorded_sales_data = pos_recorded_data[0]["sales_data"]

    # Convert json string in to json format
    recorded_sales_data = json.loads(recorded_sales_data)

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Refund total
    refund_total = 0

    # Total profit
    total_profit = 0

    # Total units
    total_units = 0

    # Index
    list_index = 0

    try:
        # Begin transaction
        db_helper.begin_transaction()

        # Itherate products to refund
        for product_service in products_services_data:
            try:    
                # Units to refund
                units_to_refund = int(escape(product_service["units"]))

                # Product or service id
                product_or_service_id = int(escape(product_service["id"]))
            except ValueError:
                abort(400, description="Something wen't wrong! Try again!")

            # Itherate recorded sales data
            for data in recorded_sales_data:
                # Product or service recorded
                product_or_service_id_recorded = data["id"]

                if product_or_service_id == product_or_service_id_recorded:
                    # Units recorded
                    units_recorded = data["units"]

                    # Cost price
                    sell_price = data["sell_price"]

                    # Product or service refund
                    refund_cost = round(float(units_to_refund) * sell_price,2)

                    # Increment refund total
                    refund_total += refund_cost

                    # Ensure units to refund are equal the amount of units already recorded,
                    # if so remove from pos_recorded_data
                    if float(units_to_refund) == units_recorded:
                        # Remove registry
                        recorded_sales_data.pop(list_index)

                    elif float(units_to_refund) < units_recorded:
                        # Update data recorded
                        data["units"] -= units_to_refund
                        data["total"] -= refund_cost
                    else:
                        # Ensure user doenst change select options elements inner html
                        abort(400, description="Units to refund can't be higher than already recorded units sold!")

                    if data["type"] == "Product":
                        # Update product sale
                        db_helper.update_product_sales(product_or_service_id, refund_cost, units_to_refund, date.today(), incre=False)
            
                        # Query product financial info
                        product_financial_info = db_helper.query_product_financial(product_or_service_id)

                        # Get product sell price
                        product_cost_price = product_financial_info[0]["cost_price"]

                        # Calculate product profit
                        product_profit = round((sell_price - product_cost_price) * float(units_to_refund), 2)

                        # Update product profit
                        db_helper.update_product_profit(product_or_service_id, product_profit, date.today(), incre=False)

                        # Increment total_profit
                        total_profit += product_profit

                        # Update product stock
                        db_helper.update_product_stock(product_or_service_id, units_to_refund, "sale_refund")

                        # Insert product movement
                        db_helper.insert_product_movement(108, units_to_refund, datetime.now(), refund_cost, product_or_service_id)

                        # Stop second loop
                        break
                    else:
                         # Update service sales
                        db_helper.update_service_sales(product_or_service_id, refund_cost, units_to_refund, date.today(), incre=False)

                        # Insert product movement
                        db_helper.insert_service_movement(108, units_to_refund, datetime.now(), refund_cost, product_service["id"])

                        # Query service info
                        service_info = db_helper.query_service(product_or_service_id)

                        # Get service sell price
                        service_cost_price = service_info[0]["cost_price"]

                        # Calculate service profit
                        service_profit = round((sell_price - service_cost_price) - float(units_to_refund), 0) 

                        # Increment total_profit
                        total_profit += service_profit

                        # Update service profit
                        db_helper.update_service_profit(product_or_service_id, service_profit, date.today(), incre=False)

                        # Query products associated with service
                        service_products = db_helper.query_service_products(product_or_service_id)

                        # Itherate service products list and update products stock
                        for product in service_products:
                            # Update product stock
                            db_helper.update_product_stock(product["id"], product["stock"], "sale_refund")
                        
                        # Stop second loop
                        break
                        
                data["total"] = round(data["total"], 2)

            # Increment total_units
            total_units += units_to_refund

        # Round refund total and total profit to two decimals
        refund_total = round(refund_total,2)
        total_profit = round(total_profit,2)

        # Update company sales
        db_helper.update_company_sales(date.today(), round(refund_total, 2), total_units, incre=False)

        # Update company profit
        db_helper.update_company_profit(date.today(), round(total_profit, 2), incre=False)

        # Query pos id
        pos_id = pos_db.execute("SELECT id FROM pos_system WHERE user_id = ?", current_user.id)
        pos_id = pos_id[0]["id"]

        # Ensure recored sales data is not empty
        if recorded_sales_data:
            # Update sales data and total
            pos_db.execute("UPDATE pos_sales_records SET total = total - ?, sales_data = ? WHERE id = ?", refund_total, json.dumps(recorded_sales_data), sale_id)
    
            # Decrement pos sales from pos database
            pos_db.execute("UPDATE pos_sales SET total = total - ?  WHERE date = ? AND pos_id = ?",  refund_total, date.today(), pos_id)
        else:
            # Delete recorded sale
            pos_db.execute("DELETE FROM pos_sales_records WHERE id = ?", sale_id)

            # Decrement pos sales and clients from pos database
            pos_db.execute("UPDATE pos_sales SET total = total - ?, clients = clients - 1 WHERE date = ? AND pos_id = ?", refund_total, date.today(), pos_id)

        # Commit transaction
        db_helper.commit()

    except (ValueError, RuntimeError, TypeError, AttributeError, KeyError):
        # If some error in transaction rollback
        db_helper.rollback()

        # Stop function and send Error
        abort(400, description="Something wen't wrong! Try again later!")

    return jsonify({"success_message": f"<span class='color-black'>Products refunded with success! Refund client: </span><span class='personal-blue-color'>{currency(refund_total)}</span>"})

@app.route("/refund_sale", methods=["POST"])
def pos_refund_sale():
    """ Refund sale request by user and send success message """

    # Sale id
    sale_id = request.data.decode("utf-8")

    # Escape special characters
    sale_id = escape(sale_id)

    # Get sale information
    sale_info = pos_db.execute("SELECT * from pos_sales_records WHERE id = ?", sale_id)

    # Get sales data from sale information
    sales_data = json.loads(sale_info[0]["sales_data"])

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Get refund total
    refund_total = sale_info[0]["total"]

    # Refund units total
    total_units = 0

    # Refund total profit
    total_profit = 0

    try:
        # Begin transaction
        db_helper.begin_transaction()
    
        for data in sales_data:
            # Get units to refund from sale

            units_to_refund = data["units"]

            # Get total to refund
            sale_total = data["total"]

            # Increment total units to refund
            total_units += units_to_refund

            if data["type"] == "Product":
                # Query product
                product_financial = db_helper.query_product(data["id"])

                # Product sell price
                cost_price = product_financial[0]["cost_price"]

                # Calculate product profit
                product_profit = round((data["sell_price"] - cost_price) * float(units_to_refund),2)

                # Increment total profit
                total_profit += product_profit
                    
                # Update product sale
                db_helper.update_product_sales(data["id"], sale_total, units_to_refund, date.today(), incre=False)
                
                # Update product profit
                db_helper.update_product_profit(data["id"], product_profit, date.today(), incre=False)
              
                # Update product stock
                db_helper.update_product_stock(data["id"], units_to_refund, "sale_refund")

                # Insert product movement
                db_helper.insert_product_movement(108, units_to_refund, datetime.now(), sale_total, data["id"])
            else:
                # Update service sales
                db_helper.update_service_sales(data["id"], sale_total, units_to_refund, date.today(), incre=False)

                # Query service info
                service_info = db_helper.query_service(data["id"])

                # Get service sell_price
                service_cost_price = service_info[0]["cost_price"]

                # Calculate service profit
                service_profit = round((data["sell_price"] - service_cost_price) * float(units_to_refund), 2)

                # Increment total profit
                total_profit += service_profit

                # Update service profit
                db_helper.update_service_profit(data["id"], service_profit, date.today(), incre=False)

                # Query products associated with service
                products_associated = db_helper.query_service_products(data["id"])

                # Update products stock associated with service
                for product in products_associated:
                    # Update product stock
                    db_helper.update_product_stock(product["product_id"], product["stock"], "refund_sale")

                # Insert service movement
                db_helper.insert_service_movement(108, f"-{units_to_refund}", datetime.now(), sale_total, data["id"])

        refund_total = round(refund_total, 2)

        total_profit = round(total_profit, 2)

        # Update company sales
        db_helper.update_company_sales(date.today(), refund_total, total_units, incre=False)

        # Update company profit
        db_helper.update_company_profit(date.today(), refund_total, incre=False)

        # Query pos id
        pos_id = pos_db.execute("SELECT id FROM pos_system WHERE user_id = ?", current_user.id)

        # Update pos sales
        pos_db.execute("UPDATE pos_sales SET total = total - ?, clients = clients - 1 WHERE date = ? AND pos_id = ?", refund_total, date.today(), pos_id[0]["id"])

        # Delete sale from pos_sales_records
        pos_db.execute("DELETE FROM pos_sales_records WHERE id = ?", sale_id)

        # Commit transaction
        db_helper.commit()

    except (ValueError, RuntimeError, TypeError, AttributeError, KeyError):

        # Rollback transaction
        db_helper.rollback()

        # Stop function and send Error
        abort(400, description="Something wen't wrong!")

    return jsonify({"success_message": f"<span class='color-black'>Sale refunded with success! Refund client: </span><span class='personal-blue-color'>{currency(refund_total)}</span>"})
                   
@app.route("/products_and_services")
@login_required
def products_and_services():
    """ Render 'products_and_services.html and return template as response """
    
    # Return rendered 'products_system.html'
    return render_template("products_and_services_templates/products_and_services.html")

@app.route("/stocks_manager")
@login_required
def stocks_manager():
    """ Render 'stocks_manager.html' and return template """
    
    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Query all user products
    products = db_helper.query_all_products()

    return render_template("stocks_manager_templates/stocks_manager.html", products=products, family_group=CATEGORIES, waste_motives=WASTE_MOTIVES)

@app.route("/register_order")
@login_required
def register_orders():
    """ Render 'register_order.html """

    form = registerProductInOrderForm()

    # Return rendered 'orders.html' with rendered order_list_table_html
    return render_template("register_order_templates/register_order.html", form=form)

@app.route("/expenses")
@login_required
def expenses():
    """ Render 'expenses.html' """
    # Create Flask-WTF form to register expense
    register_expense_form = registerExpenseForm()

    # Create Flask-WTF form to check expense
    check_expense_form = checkExpensesForm()
    
    # Actual date
    today = date.today()

    # Get allowed insert dates
    insert_dates = get_allowed_insert_or_edit_expense_dates(today)

    register_expense_form.month_year_dates.choices = insert_dates
    register_expense_form.expenses.choices = [(expense["expense_id"], expense["expense_description"]) for expense in EXPENSE_TYPES]
        
    # Initiate Database_helper object
    db_helper = current_user.db_connection
    
    # Query user expenses
    user_expenses = db_helper.query_all_expenses()

    # Date to check expense
    check_month = []
    check_year = []

    # Append user expenses to check month and check year lists
    for exp in user_expenses:
        if exp["expense_month"] not in check_month:
            check_month.append(exp["expense_month"])
        if exp["expense_year"] not in check_year:
            check_year.append(exp["expense_year"])

    check_expense_form.year.choices = check_year
    check_expense_form.month.choices = check_month

    # Return rendered 'expenses.html'
    return render_template("expenses_templates/expenses.html", register_expense_form=register_expense_form, check_expense_form=check_expense_form)

@app.route("/human_resources")
@login_required
def human_resources():
    """ Render human_resources.html and return template """

    # Workload hours a day
    workloadhours_day = [1,2,3,4,5,6,7,8,9,10]

    # Workload hours a week
    workloadhours_week = []

    # Roles
    roles = ["Manager", "Chief", "Sub chief", "Worker"]

    # 0,1,2,3,4,5 ... 40
    for i in range(1, 41):
        workloadhours_week.append(i)

    # Actual date
    today = date.today()

    # Year
    year = relativedelta(years=1)

    # Maximum worker born date - Maximum age to work - 18 years old
    maximum_worker_born_date = today - year * 18

    # Initiate Database_helper object 
    db_helper = current_user.db_connection

    # Company workers
    workers = db_helper.query_workers()

    return render_template("/human_resources_templates/human_resources.html", workloadhours_day=workloadhours_day, workloadhours_week=workloadhours_week, sections=SECTIONS, roles=roles, maximum_worker_born_date=maximum_worker_born_date, workers=workers)

@app.route("/inventories")
@login_required
def invetories():
    """ Render invetories.html and return template """

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Query closed inventories
    closed_inventories = db_helper.query_closed_inventories()

    # Inventories dates list for user search
    inventories_date = []

    for inventory in closed_inventories:
        # Inventory date
        inventory_date = f"{inventory['month_created']}/{inventory['year_created']}"
        
        # Ensure inventory date is not already listed, else append
        if inventory_date not in inventories_date:
            inventories_date.append(inventory_date)

    return render_template("/inventories_templates/inventories.html", categories=CATEGORIES, inventories_date=inventories_date)

@app.route("/sales_and_wastes_analysis", methods=["GET", "POST"])
@login_required
def sales_and_wastes_analysis():
    """ Render sales_and_wastes_analyzis.html and return template """

    # Initiate Database_helper
    db_helper = current_user.db_connection

    # Query movements dates
    movements_dates = db_helper.query_movements_dates([102, 103, 104, 105, 106, 107])
    
    # Years and months years select options
    years = []
    months_years = []

    # Itherate movements_dates
    for dates in movements_dates:
        # Split year and month
        year,month,_ = dates["date"].split("-")

        # Ensure year is listed already else append
        if year not in years:   
            years.append(year)
        
        # Month/Year
        month_year = f"{month}/{year}"

        # Ensure month_year is not listed else append
        if month_year not in months_years:
            months_years.append(month_year)

    # Return sales_and_wastes_analysis.html rendered 
    return render_template("/sales_and_wastes_analysis_templates/sales_and_wastes_analysis.html", years=years, months_years=months_years)

@app.route("/mensal_reports")
@login_required
def mensal_reports():
    """ Render mensal_reports.html """

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Query movements dates
    dates = db_helper.query_movements_dates()

    # Cleaned year and month dates empty list
    cleaned_dates = []

    # Get date month and year
    for movement_date in dates:
        # Split year and month
        year, month, _ = movement_date["date"].split("-")

        # Convert year and month to integer
        year = int(year)
        month = int(month)

        # Cleaned date
        cleaned_date = f"{month}/{year}"

        cleaned_dates.append(cleaned_date)

    return render_template("mensal_report_templates/mensal_reports.html", dates=cleaned_dates)


@app.route("/register_products", methods=["POST"])
def register_products():
    """ Register products """

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Query products from temp register list
    register_temp_products = db_helper.query_all_products_from_temp_register_list()
    
    # Insert products from temp_register_list table to products table
    try:
        # Begin transaction
        db_helper.begin_transaction()

        # Register products
        db_helper.insert_products()

        # Delete products from temp_register_list table
        db_helper.delete_all_products_from_temp_register_list()

        # Commit transaction
        db_helper.commit()

    except (ValueError, TypeError, KeyError):
        # Register products
        db_helper.insert_products()

        # Rollback transaction
        db_helper.rollback()
    
        # Abort function and send Error
        abort(400, description="Something wen't wrong!")

    # Create empty html list
    html_list = ""

    # Append products info
    for product in register_temp_products:
        html_list += f"<li class='list-group-item'>Description: <span class='f-bold personal-blue-color'>{product['description']}</span> / Bar code: <span class='f-bold personal-blue-color'>{product['bar_code']}</span> / Unity measurement: <span class='f-bold personal-blue-color'>{product['unity_m']}</span> / Category: <span class='f-bold personal-blue-color'>{CATEGORIES[int(product['category']) - 1001]['category']}</span> / Sub category: <span class='f-bold personal-blue-color'>{CATEGORIES[int(product['category']) - 1001]['sub_categories'][int(product['category']) * 10 - int(product['category']) * 10 + 1]['sub_category']}</span> / Stock: <span class='f-bold personal-blue-color'>{product['stock']}</span> / Cost price: <span class='f-bold personal-blue-color'>{currency(product['cost_price'])}</span> / Sell price: <span class='f-bold personal-blue-color'>{currency(product['sell_price'])}</span> / Margin: <span class='f-bold personal-blue-color'>{percentage(product['margin_percentage'])}</span> </li>"

    # Create html with register sucess info to send
    html = f"""
            <div class="mt-3 mb-3">
                <h5 class="personal-blue-color">Product/s registered with sucess!</h5>
            </div>
            <hr></hr>
            <div class="col-lg-12 text-center">
                <h6 class="personal-blue-color">Products registered</h6>
            </div> 
            <div class='col-lg-12 p-1 border'>
                <ul class="list-group list-group-flush">
                {html_list}
                </ul>
            </div>
            <hr></hr>
            <div class="small-size f-bold color-black">Consult your products in 'My products and services'.</div>
            """

    # Return register sucess info html
    return jsonify({"register_list_sucess_html": html})

@app.route("/register_service", methods=["POST"])
def register_service():
    """ Register service """

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Get form data sended in request
    form_data = request.get_json()

    # Clean form data white spaces
    form_data = clean_form_white_spaces(form_data)

    # Create Flask-WTF form to register service
    form = registerServiceForm(form_data=form_data)

    # Update products associated field entries
    entries = 0
    for k,v in form_data.items():
        if k.startswith("products_associated"):
            entries += 1

    entries = entries / 3

    form.products_associated.min_entries = entries
    form.products_associated.max_entries = entries

    # User products
    products = db_helper.query_all_products()

    # Create choices with products description
    choices = [(product["id"], product["description"]) for product in products]

    items_values = []

    # Update products field choices 
    for item in form.products_associated:
        if item.form.product.data not in items_values:
            items_values.append(item.form.product.data)

        for i in range(len(choices)):
            if choices[i][0] in items_values:
                choices.pop(i)

        item.form.product.choices = choices 

    print(form.products_associated.data)

    if form.validate_on_submit():
        # Convert cost price and sell price to float
        service_cost_price = float(form.cost_price.data)
        service_sell_price = float(form.sell_price.data)

        print(service_cost_price)

        # Ensure cost price and sell price are higher than 0 and if cost price is lower than sell price
        if service_cost_price >= service_sell_price:
            abort(400, description="Sell price must be higher than cost price.")

        # Get margin percentage
        margin_percentage = calculate_price_margin(service_cost_price, service_sell_price)

        # Validate service
        validate_service(form.service_description.data.upper(), form.products_associated.data)

        try:
            # Begin transaction
            db_helper.begin_transaction()

            # Insert service
            db_helper.insert_service(form.service_description.data.upper(), round(service_cost_price,2), round(service_sell_price,2), round(margin_percentage,2), form.products_associated.data)

            # Commit transaction
            db_helper.commit()

        except (ValueError, RuntimeError, TypeError, AttributeError, KeyError):

            # Rollback transaction
            db_helper.rollback()

            # Abort function and send Error
            abort(500, description="Something wen't wrong!")
 
        products_and_stocks = []

        # Itherate products and stocks
        for p_and_s in form.products_associated.data:
            # Query product 
            product = db_helper.query_product(p_and_s["product"])

            # Product description
            product_description = product[0]["description"]

            products_and_stocks.append({"description": product_description, "stock_associated": float(p_and_s["stock_associated"])})

    else:
        # Create HTML with errors
        errors = ""
        for _, error in form.errors.items():
            print(error)
            if isinstance(error[0], str):
                errors += f"<p>{error[0]}</p>"
            else:
                for _, v in error[0].items():
                    errors += f"<p>{v[0]}</p>"

        abort(400, description=errors)

    # Render register_service_sucess.html
    sucess_html = render_template("/products_and_services_templates/register_service_sucess.html", service_description=form.service_description.data, service_cost_price=service_cost_price, service_sell_price=service_sell_price, margin_percentage=margin_percentage, products_and_stocks=products_and_stocks)
    
    return jsonify({"success_response": sucess_html})

@app.route("/register_order", methods=["POST"])
def register_order():
    """ Register order and render sucess order register with report """

    # Order total
    order_total = request.get_json()[0]

    # Convert to float
    order_total = float(order_total)

    # Other order encharges
    order_other_encharges = request.get_json()[1]

    # Convert to float
    order_other_encharges = float(order_other_encharges)

    # Initiate Database_helper
    db_helper = current_user.db_connection

    # Query all user registered products
    all_products = db_helper.query_all_products()

    # Query all products from order_list
    order_list_products = db_helper.query_all_products_from_order_list()

    # Order product updates report
    order_product_updates = []

    # Service associated changes report
    services_updates = []
    
    try:
        # Begin transaction
        db_helper.begin_transaction()

        # Itherate order products 
        for order_product in order_list_products:
            # Orders products description, bar code, cost price and sell price
            order_product_description = order_product["description"] 
            order_product_cost_price = order_product["cost_price"]
            order_product_sell_price = order_product["sell_price"]
            order_product_quantity = order_product["quantity"]
            
            # Update message
            update_message = ""
            
            # All products index
            all_products_order_product_index = 0

            # Itherate registered products
            for registered_product in all_products:
                registered_product_description = registered_product["description"]

                # Ensure order product is registered
                if order_product_description == registered_product_description:

                    registered_product_id = registered_product["id"]
                    registered_product_cost_price = registered_product["cost_price"]
                    registered_product_sell_price = registered_product["sell_price"]
                    registered_product_stock = registered_product["stock"]

                    # Update stock
                    db_helper.update_product_stock(registered_product_id, order_product_quantity, "order_entry")
                    update_message += f"Product: <span class='color-black f-bold'>{registered_product_description}</span> | Stock changed: <span class='f-bold sucess-message'>{registered_product_stock}</span> -> <span class='f-bold sucess-message'>{registered_product_stock + order_product_quantity} </span> "

                    # Ensure cost price or sell price changed
                    cost_price_changed = False
                    if order_product_cost_price != registered_product_cost_price:
                        cost_price_changed = True
                        update_message += f"| Cost price changed: <span class='f-bold sucess-message'>{currency(registered_product_cost_price)}</span> -> <span class='f-bold sucess-message'>{currency(order_product_cost_price)}</span> "

                    sell_price_changed = False
                    if order_product_sell_price != registered_product_sell_price:
                        sell_price_changed = True
                        update_message += f"| Sell price changed: <span class='f-bold sucess-message'>{currency(registered_product_sell_price)}</span> -> <span class='f-bold sucess-message'>{currency(order_product_sell_price)}</span> "
            
                    # Remove product from all products list to reduce search
                    del all_products[all_products_order_product_index]

                    # Increment index 
                    all_products_order_product_index += 1

                    # Append update message
                    order_product_updates.append(update_message)

                    if cost_price_changed or sell_price_changed:
                        # Get new product margin profit
                        margin_percentage = calculate_price_margin(order_product_cost_price, order_product_sell_price)

                        # Product unity of measurement
                        product_unity_m = registered_product["unity_m"]

                        # Update product prices
                        db_helper.update_product_financial(registered_product_id, order_product_cost_price, order_product_sell_price, margin_percentage, product_unity_m)

                    if cost_price_changed:
                        # Query services associated
                        services_associated = db_helper.query_services_associated(registered_product_id)

                        # Ensure product have services associated
                        if len(services_associated) > 0: 
                            for service in services_associated:
                                # Get service basic and financial information
                                service_info = db_helper.query_service(service["id"])
                                service_description = service_info[0]["description"]

                                # Append service update message
                                services_updates.append(f"Service: <span class='f-bold color-black'>{service_description}</span> affected by <span class='f-bold color-black'>{order_product_description} cost price change!</span>")
                            
                            break
        # Global order total
        global_order_total = float(order_total) + float(order_other_encharges)
        
        # Render sucess_order_register.html with info
        sucess_order_register_html = render_template("/register_order_templates/sucess_order_register.html", order_total=order_total, order_other_encharges=order_other_encharges, global_order_total=global_order_total, order_product_updates=order_product_updates, services_updates=services_updates) 

        # Actual date
        today = date.today()

        # Insert products entry movements in to movements table
        for product in order_list_products:
            # Product quantity
            product_quantity = product["quantity"]

            # Calculate product ordered total 
            product_order_total = product_quantity * product["cost_price"]

            # Query product id
            product_id = db_helper.query_product_id(product["description"])
            product_id = product_id[0]["id"]

            # Insert product movement
            db_helper.insert_product_movement(101, product_quantity,  datetime.now(), round(product_order_total, 2), product_id)

        # Convert order products in to a string
        order_list_products = json.dumps(order_list_products[0])

        # Insert order
        db_helper.insert_order(order_list_products, order_total, today)

        # Commit transaction
        db_helper.commit()

    except (ValueError, RuntimeError, TypeError, AttributeError, KeyError):

        # Rollback transaction
        db_helper.rollback()

        # Abort function and send Error
        abort(400, description="Something wen't wrong!")


    # Return sucess order register html
    return jsonify({"sucess_order_register_html": sucess_order_register_html})

@app.route("/register_worker", methods=["POST"])
def register_worker():
    """ Register worker """

    # Worker data
    worker_data = request.get_json()

    worker_fullname = worker_data["fullname"]
    worker_adress = worker_data["adress"]
    worker_contact = worker_data["contact"]
    worker_born_date = worker_data["born_date"]
    worker_section = worker_data["section"]
    worker_role = worker_data["role"]
    worker_workload_day = worker_data["workload_day"]
    worker_workload_week = worker_data["workload_week"]
    worker_base_salary = worker_data["base_salary"]

    # Capitalize worker fullname and adress
    worker_fullname = capitalize_string(worker_fullname)
    worker_adress = capitalize_string(worker_adress)

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Query all workers
    workers = db_helper.query_workers()

    # Set a worker number to new worker
    worker_number = set_worker_number(workers)

    # Register worker
    db_helper.insert_worker(worker_number, worker_fullname, worker_adress, worker_contact, worker_born_date, worker_section, worker_role, worker_workload_day, worker_workload_week, worker_base_salary)

    return jsonify({"success_message": "Worker registered with sucess!"})

@app.route("/create_inventory", methods=["POST"])
def register_inventory():
    """ Create inventory and insert in inventories table """

    # Products ids to create inventory
    products_ids = request.get_json()

    if not products_ids:
        abort(400, description="Please select products!")

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Ensure products are registered
    for product_id in products_ids:
        # Query product
        try:
            _ = db_helper.query_product(product_id)
        except IndexError:
            abort(400, description="Product not registered!")

    # Today date
    today = date.today()

    # Date with hours
    actual_date = datetime.now()

    # Query all inventories
    inventories = db_helper.query_inventories()

    # Get a inventory number
    try:
        inventory_number = inventories[-1]["inventory_number"] + 1
    except IndexError:
        inventory_number = 1000000000000

    # Create inventory
    db_helper.insert_inventory(inventory_number, actual_date, today.year, today.month, "open")

    # Query last inventory
    last_open_inventory_inserted = db_helper.query_open_inventories()

    # Inventory id
    inventory_id = last_open_inventory_inserted[-1]["id"]

    # Insert inventory information in inventory_products table
    for product_id in products_ids:
        # Query all product info
        product = db_helper.query_product(product_id)

        # Insert information
        db_helper.insert_product_in_inventories_products(inventory_id, product_id, product[0]["stock"], product[0]["cost_price"], "not counted")

    sucess_html = f"<h8 class='color-black'>Inventory with number <span class='personal-blue-color f-bold'>{inventory_number}</span> created with sucess!</h8>"

    return jsonify({"sucess_message": sucess_html })

@app.route("/register_inventory_counts", methods=["POST"])
def register_inventory_counts():
    """ Register inventory_counts """

    # Data
    data = request.get_json()

    print(data)

    # Inventory id
    inventory_id = data["inventory_id"]

    # Inititate Database_helper object
    db_helper = current_user.db_connection

    # Ensure inventory is registered
    inventory = db_helper.query_inventory(inventory_id)
    
    if not inventory:
        abort(400, description="Inventory doesn't exist!")

    # Counts
    counts = data["counts"]

    # Ensure user insert counts
    if not counts:
        abort(400, description="Please input a valid count value!")

    # Ensure product is registered and product count values are valid
    for count in counts:
        # Query product info
        product_info = db_helper.query_product(count["product_id"])

        # Ensure product is registered
        if not product_info:
            abort(400, description="Product is not registered.")

        # Product count value
        product_count_value = count["stock_value"]

        # Convert count value to float
        try:
            product_count_value = float(product_count_value)
        except ValueError:
            abort(400, description="Please input a valid count value!")

        # Ensure count value is not less than 0 and was inputed
        if product_count_value < 0:
            abort(400, description="Count must be equal or higher than 0!")
   
    # Inventory status
    inventory_status = inventory[0]["status"]

    products_count = 0

    # Ensure inventory status is in recount or open
    if inventory_status == "open":
        # Query inventories products count
        _, products_count = db_helper.query_inventory_products(inventory_id, 0)
        print(products_count)
    else:
        # Query inventory recount products count
        _, products_count = db_helper.query_recount_inventory_products(inventory_id, 0)

    # Ensure all products have been counted
    if products_count != len(counts):
        abort(400, description="Please insert all products count before submit!")
        
    # Ids list
    products_ids = []

    # Insert counts in inventory_products table
    for count in counts:
        db_helper.update_product_inventory_count(inventory_id, count["product_id"], count["stock_value"])
        products_ids.append(count["product_id"])

    # Update inventory status in inventories table
    db_helper.update_inventory_status(inventory_id, "counted")

    # Update products status in inventories_products table
    db_helper.update_inventory_products_status(inventory_id, products_ids, "counted")

    sucess_html = f"<h8 class='color-black'>Inventory number: <span class='personal-blue-color f-bold'>{inventory[0]['inventory_number']}</span> counts submitted with sucess!</h8>"

    # Return sucess_html
    return jsonify({"sucess_html": sucess_html})

@app.route("/register_finish_inventory", methods=["POST"])
def register_finish_inventory():
    """ Finish inventory, update inventories tables, insert products movement into movements table """

    # Inventory_id
    inventory_id = request.data.decode("utf-8")

    # Inititate Database_helper object
    db_helper = current_user.db_connection

    # Ensure inventory is registered
    try:
        inventory = db_helper.query_inventory(inventory_id)
    except IndexError:
        abort(400, description="Inventory doesn't exist!")

    # Inventory number
    inventory_number = inventory[0]["inventory_number"]

    # Query products information from products table with product information from inventories_products table
    finish_inventory_products = db_helper.query_inventory_products(inventory_id, all_to_search=True) 

    # Actual date
    today = date.today()

    products_ids = []

    # Query inventory global count diff and total 
    global_count_diff_and_total = db_helper.query_inventory_diff_and_total(inventory_id)
    global_diff = global_count_diff_and_total[0]["stock_diff"]
    global_diff_value = global_count_diff_and_total[0]["stock_diff_value"]

    try:
        # Begin transaction
        db_helper.begin_transaction()

        # Itherate finish products
        for product in finish_inventory_products:
            # Product stock diff
            product_stock_diff = product["stock_diff"]

            # Product stock diff value
            product_stock_diff_value = product["stock_diff_value"]

            # Stock inserted
            stock_inserted = product["stock_counted"]

            # Product id
            product_id = product["id"]

            # Ensure product is registered
            product_info = db_helper.query_product(product_id)

            if not product_info:
                abort(400, description="Product is not registered.")

            # Ensure stock diff is negative or positive to handle movement type and movement total
            if product_stock_diff < 0:
                # Split '-' from product_stock_diff_value
                product_stock_diff_value = float(str(product_stock_diff_value).split("-")[-1])

                # Inventory waste movement id
                movement_type_id = 105

                # Insert regularization in non_indentified_wastes table
                db_helper.insert_product_non_identified_waste(today, product_stock_diff_value, product_id)

                # Insert waste in to companies_wastes table
                db_helper.insert_company_waste(today, product_stock_diff_value)
                    
                # Insert into product_wastes table
                db_helper.insert_product_waste(today, product_stock_diff_value, product_id)
            else:
                # Inventory benefit movement id
                movement_type_id = 106

                # Insert product regularization benefit
                db_helper.insert_product_benefit(product_id, today, product_stock_diff_value)

            # Insert product movement
            db_helper.insert_product_movement(movement_type_id, product_stock_diff, datetime.now(), product_stock_diff_value, product_id)

            # Update product stock
            db_helper.update_product_stock(product_id, stock_inserted, "inventory")

            # Append id to products ids list
            products_ids.append(product_id)
        
        if global_diff > 0:
            global_diff_html = f"<span class='sucess-message f-bold'>{benefit_un(global_diff)}</span>"
            global_diff_value_html = f"<span class='sucess-message f-bold'>{benefit(global_diff_value)}</span>"
        else:
            global_diff_html = f"<span class='error-message f-bold'>{global_diff}</span>"
            global_diff_value_html = f"<span class='error-message f-bold'>{currency(global_diff_value)}</span>"

        # Update inventory status
        db_helper.update_inventory_status(inventory_id, "closed")

        # Update inventory products status
        db_helper.update_inventory_products_status(inventory_id, products_ids, "closed")

        # Commit transaction
        db_helper.commit()

    except (ValueError, RuntimeError, TypeError, AttributeError, KeyError):

        # Rollback transaction
        db_helper.rollback()

        # Abort function and send Error
        abort(500, description="Something wen't wrong!")

    # Sucess html
    sucess_html = f"""
                    <div class='color-black'>
                      <h8>Inventory <span class='personal-blue-color f-bold'>{inventory_number}</span> finished with sucess!</h8>
                      <ul class="list-group list-group-flush mt-3 mb-3">
                        <li class="list-group-item">Difference: <span class='personal-blue-color f-bold'>{global_diff_html}</span></li>
                        <li class="list-group-item">Difference(€): <span class='personal-blue-color f-bold'>{global_diff_value_html}</span></li>
                      </ul>
                    </div>
                   """
    
    return jsonify({"sucess_html": sucess_html})

@app.route('/register_product_waste_or_regularization', methods=["POST"])
def register_product_waste_or_regularization():
    """  Regularize product stock """
    
    # Get form data
    form_data = request.get_json()

    # Get extra form data with product id and movement type
    extra_form_data = json.loads(form_data["extra_form_data"])

    try:
        stock_movement_type = extra_form_data["movement_type"]

        if stock_movement_type == "waste":
            # Create Flask-WTF register waste
            form = registerWasteForm(form_data=form_data)
        else:
            # Create Flask-WTF register regularization form
            form = registerRegularizationForm(form_data=form_data)
    except KeyError:
        abort(400, description="No motive selected!")  
  
    # Initiate Database_helper object
    db_helper = current_user.db_connection

    product_id = extra_form_data["product_or_service_id"]
  
    stock_movement_type = extra_form_data["movement_type"]

    # Query product
    product_info = db_helper.query_product(product_id)

    if not product_info:
        abort(400, description="Product not registered!")

    # Ensure product is not in inventory
    product_inventories = db_helper.query_product_inventories(product_id, status="open")

    if product_inventories:
        abort(400, description="Action denied! Product in inventory.")


    if form.validate_on_submit():

        stock_inserted = float(form.stock.data)

        # Get actual date
        today = date.today()
        
        # Movement total
        total = 0

        # Product cost price
        product_cost_price = product_info[0]["cost_price"]

        # Product description
        product_description = product_info[0]["description"]

        # Product actual stock
        product_actual_stock = product_info[0]["stock"]

        # Sucess message
        sucess_message = ""
    
        # Actual date
        today = date.today()

        try:
            db_helper.begin_transaction()

            if stock_movement_type == 'regularize':

                # Ensure stock inserted is not equal to product actual stock
                if stock_inserted == product_actual_stock:
                    abort(400, description="Stock inserted equal to actual stock.")

                # Calculate regularization
                total, stock_diff = calculate_regularization_total(product_actual_stock, stock_inserted, product_cost_price)

                if stock_diff > 0:
                    # Insert product regularization benefit
                    db_helper.insert_product_benefit(product_id, today, total)

                    regularization_html = f"<span class='f-bold sucess-message'>{benefit(total)}</span>"

                    # Regularization benefit movement id
                    movement_type_id = 103
                else:
                    # Insert regularization in non_indentified_wastes table
                    db_helper.insert_product_non_identified_waste(today, total, product_id)

                    # Insert waste in to companies_wastes table
                    db_helper.insert_company_waste(today, total)
                    
                    # Insert into product_wastes table
                    db_helper.insert_product_waste(today, total, product_id)

                    # Html sucess message 
                    regularization_html = f"<span class='f-bold error-message'>{currency(total)}</span>"

                    # Regularization waste movement id
                    movement_type_id = 102

                # Sucess message
                sucess_message = f"<span class='color-black'>Product <span class='f-bold'>{product_description}</span> regularized with sucess! Regularization total: {regularization_html}"

                # Update movements table
                db_helper.insert_product_movement(movement_type_id, stock_diff, datetime.now(), total, product_id)

            elif stock_movement_type == "waste":
                
                # Calculate waste
                total = calculate_waste_total(stock_inserted, product_cost_price)

                # Motive
                motive = form.waste_motives.data

                # Sucess message
                sucess_message = f"<span class='color-black'>Product <span class='f-bold'>{product_description}</span> wasted with sucess! Waste total: <span class='f-bold error-message'>{currency(total)}</span>"

                movement_type_id = 104

                # Update movements table
                db_helper.insert_product_movement(movement_type_id, f"-{stock_inserted}", datetime.now(), total, product_id)

                # Insert waste in indentified_wastes table
                db_helper.insert_product_identified_waste(today, total, motive, product_id)

                # Insert waste in to companies_wastes table
                db_helper.insert_company_waste(today, total)
                    
                # Insert into product_wastes table
                db_helper.insert_product_waste(today, total, product_id)
            
            # Updade product stock
            db_helper.update_product_stock(product_id, stock_inserted, stock_movement_type)

            db_helper.commit()

        except (ValueError, RuntimeError, TypeError, AttributeError, KeyError):

            db_helper.rollback()
            abort(500, description="Something wen't wrong!")

        return jsonify({"success_response": sucess_message})

    else:
        # Create HTML with errors
        errors = ""
        for _, error in form.errors.items():
            print(error)
            if isinstance(error[0], str):
                errors += f"<p>{error[0]}</p>"
            else:
                for _, v in error[0].items():
                    errors += f"<p>{v[0]}</p>"

        # Abort function and send errors as response
        abort(400, description=errors)
    

@app.route('/register_service_waste_or_regularization', methods=["POST"])
def register_service_waste():
    """  Register service identified waste """

     # Get form data
    form_data = request.get_json()

    # Create Flask-WTF register waste or regularization form
    form = registerWasteForm(form_data=form_data)

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Get description and real stock
    extra_form_data = json.loads(form_data["extra_form_data"])

    service_id = extra_form_data["product_or_service_id"]
   
    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Query product
    service_info = db_helper.query_service(service_id)

    if not service_info:
        abort(400, description="Service not registered!")

    if form.validate_on_submit():
        # Get actual date
        today = date.today()
        
        # Movement total
        total = 0

        # Product cost price
        service_cost_price = service_info[0]["cost_price"]
        service_description = service_info[0]["description"]

        # Actual date
        today = date.today()

        stock_inserted = float(form.stock.data)

        # Calculate waste
        total = calculate_waste_total(stock_inserted, service_cost_price)

        # Motive
        motive = form.waste_motives.data

        # Sucess message
        success_message = f"<span class='color-black'>Service <span class='f-bold'>{service_description}</span> wasted with sucess! Waste total: <span class='f-bold error-message'>{currency(total)}</span>"
        
        movement_type_id = 103

        # Update movements table
        db_helper.insert_service_movement(movement_type_id, float(f"-{stock_inserted}"), datetime.now(), total, service_id)

        # Insert waste in indentified_wastes table
        db_helper.insert_service_identified_waste(today, total, motive, service_id)

        # Insert waste in to companies_wastes table
        db_helper.insert_company_waste(today, total)

        # Query products associated with service
        service_products_associated = db_helper.query_service_products(service_id)

        # Register waste at products associated with service
        for product in service_products_associated:
            # Product id
            product_id = product["product_id"]

            # Query product price
            product_info = db_helper.query_product_financial(product_id)
            product_cost_price = product_info[0]["cost_price"]

            # Get product associated stock with service
            product_stock_associated = product["stock"]

            # Calculate product associated waste
            waste_total = (product_stock_associated * product_cost_price) * stock_inserted 

            # Insert product waste
            db_helper.insert_product_waste(date.today(), waste_total, product_id)

            # Update product stock
            db_helper.update_product_stock(product_id, product_stock_associated, "waste")

        return jsonify({"success_response": success_message})

    else:        
        # Create HTML with errors
        errors = ""
        for _, error in form.errors.items():
            print(error)
            if isinstance(error[0], str):
                errors += f"<p>{error[0]}</p>"
            else:
                for _, v in error[0].items():
                    errors += f"<p>{v[0]}</p>"

        # Abort function and send errors as response
        abort(400, description=errors)
    
@app.route("/register_registry", methods=["POST"])
def register_registry():
    """ Validate registry and insert in to purchase session """

    print(request.get_json())

    registry_data = request.get_json()[0]

    # Ensure user select a service or product
    registry_data_type = registry_data["type"]

    registry_data_id = registry_data["id"]

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    if registry_data_type == "Product": 
        # Query product
        product_info = db_helper.query_product(registry_data_id)

        # Ensure product is registered
        if not product_info:
            abort(400, description="Product not registered.")

        # Product description
        registry_description = product_info[0]["description"]

        # Product bar code
        registry_bar_code = product_info[0]["bar_code"]

    else:
        # Query service
        service_info = db_helper.query_service(registry_data_id)

        # Ensure service is registered
        if not service_info:
            abort(400, description="Service not registered.")

        registry_description = service_info[0]["description"]

        # Service bar code
        registry_bar_code = service_info[0]["bar_code"]

    # Add new key value pair to registry data with product description
    registry_data["description"] = registry_description
    registry_data["bar_code"] = registry_bar_code

    # Product sell price
    sell_price = registry_data["sell_price"]
                                       
    # Product unity m
    unity_m = registry_data["unity_m"]

    # Units to registry
    units_to_registry = int(registry_data["units"])

    # If product unity of measurement is 'UN' ensure units is an integer
    if unity_m == 'UN' and not isinstance(units_to_registry, int):
        abort(400, description="<h5 class='color-black'>Products and services with <span class='personal-blue-color'>'UN'</span> as unity of measurement can't be multiplied by decimal numbers!</h5>")

    # Ensure user insert correct data
    try:
        registry_total = round(sell_price * float(units_to_registry),2)

        # Create new key value pair in registry data with registry total
        registry_data["registry_total"] = registry_total

    except ValueError:
        abort(400, description="Something wen't wrong!")

    # Ensure if a purchase is already active, else start one
    try:
        # Get purchase list
        purchase = session["purchase"]
        
        # Append to active purchase registry data
        purchase.append(registry_data)

    except KeyError:
        # Create new purchase
        session["purchase"] = [registry_data]
    
    return jsonify({"message": "Registry inserted with success!"})

@app.route("/register_sale", methods=["POST"])
def register_sale():
    """ Validate and register POS sale """

    # Purchase info
    purchase_info = session["purchase"]

    # Get purchase total
    purchase_total = 0

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Get purchase total
    for info in purchase_info:
        # Increment registries total
        purchase_total += info["registry_total"]

    sale_data = request.get_json()

    try:
        # Cash value
        cash_value = float(sale_data["cash_input_value"])

        if cash_value < purchase_total:
            abort(400, description="Not enough money!")

        # Get change
        change = cash_value - purchase_total

        # Return success message
        success_message = f"<div class='color-black'>Sale with value of <span class='sucess-message f-bold'>{currency(purchase_total)}</span> successfully inserted! Change: <span class='sucess-message f-bold'>{currency(change)}</span></div>"

    except ValueError:
        change = 0
        # Return success message
        success_message = f"<div class='color-black'>Sale with value of <span class='sucess-message f-bold'>{currency(purchase_total)}</span> successfully inserted!</div>"

    # Divide data in two lists: products and services and sum each product and service total and units
    products_cleaned_data = []
    services_cleaned_data = []

    for info in purchase_info:
        # Get id
        product_service_id = info["id"]

        # Description
        product_service_description = info["description"]

        # Bar code
        bar_code = info["bar_code"]

        # Get units
        units = info["units"]

        # Get cost price
        sell_price = info["sell_price"]

        # Product type
        registry_type = info["type"]

        # Get total
        total = info["registry_total"]

        # Get registry type
        if registry_type == "Product":
            # Set has_product to False
            has_product = False

            # Ensure product is not listed already
            for product in products_cleaned_data:
                if product["id"] == product_service_id:
                    # Increment units already registered
                    product["units"] += units

                    # Increment total already registered
                    product["total"] += total

                    # Set has_product to True and stop loop
                    has_product = True
                    break
                    
            if not has_product:
                # Append product sale information
                products_cleaned_data.append({"id": product_service_id, "description": product_service_description,"bar_code": bar_code, "units": units, "sell_price": sell_price, "total": round(total,2), "type": registry_type})
        else:
            # Set has_product to False
            has_service = False

            # Ensure product is not listed already
            for service in services_cleaned_data:
                if service["id"] == product_service_id:
                    # Increment units already registered
                    service["units"] += units

                    # Increment total already registered
                    service["total"] += total

                    # Set has_product to True and stop loop
                    has_service = True
                    break
                    
            if not has_service:
                # Append product sale information
                services_cleaned_data.append({"id": product_service_id, "description": product_service_description, "bar_code": bar_code, "units": units, "sell_price": sell_price, "total": total, "type": registry_type})

    total_units = 0

    total_profit = 0

    try:
        # Begin transaction
        db_helper.begin_transaction()

        # Insert product sales and movements
        for product in products_cleaned_data:
            # Insert product sale
            db_helper.insert_product_sale(product["id"], date.today(), product["total"], product["units"])

            # Query product id
            product_info = db_helper.query_product_financial(product["id"])

            # Calculate product profit
            product_profit = (product["sell_price"] - product_info[0]["cost_price"]) * float(product["units"])
          
            # Increment total profit
            total_profit += product_profit

            # Insert product profit
            db_helper.insert_product_profit(date.today(), product_profit, product["id"])

            # Insert product movement
            db_helper.insert_product_movement(107, float(f"-{product['units']}"), datetime.now(), product["total"], product["id"])

            # Update product stock
            db_helper.update_product_stock(product_service_id, product["units"], "sale")

            total_units += product["units"]
        
        for service in services_cleaned_data:
            # Insert service sale
            db_helper.insert_service_sale(service["id"], date.today(), service["total"], service["units"])

            # Query service info
            service_info = db_helper.query_service(service["id"])
           
            # Calculate service profit
            service_profit = round((service["sell_price"] - service_info[0]["cost_price"]) * service["units"])
        
            # Increment total profit
            total_profit += service_profit

            # Insert service profit
            db_helper.insert_service_profit(date.today(), service_profit, service["id"])            
            
            # Insert product movement
            db_helper.insert_service_movement(107, float(f"-{service['units']}"), datetime.now(), service["total"], service["id"])

            # Query service products associated
            products_associated = db_helper.query_service_products(product_service_id)

            # Update service products associated stock
            for product in products_associated:
                # Update product stock
                db_helper.update_product_stock(product["product_id"], product["stock"], "sale")

            total_units += service["units"]

        # Insert company sale
        db_helper.insert_company_sale(date.today(), purchase_total, total_units)

        # Insert company profit
        db_helper.insert_company_profit(date.today(), total_profit)
        
        # Query pos id
        pos_id = pos_db.execute("SELECT id FROM pos_system WHERE user_id = ?", current_user.id)
        pos_id = pos_id[0]["id"]

        # Insert or update sale pos_sales_data
        try:
            # Insert pos sales
            params = (1, purchase_total, pos_id, date.today())

            # Insert pos sales
            pos_db.execute("INSERT INTO pos_sales (clients, total, pos_id, date) VALUES(?,?,?,?)", *params)
        except ValueError:
            pos_db.execute("UPDATE pos_sales SET clients = clients + ?, total = total + ? WHERE pos_id = ? AND date = ?", *params)

        # Insert pos sales record
        pos_db.execute("INSERT INTO pos_sales_records (pos_id, datetime, total, sales_data, payment_method, change) VALUES (?,?,?,?,?,?)", pos_id, datetime.now(), round(purchase_total,2), json.dumps(products_cleaned_data + services_cleaned_data), sale_data["payment_method"], round(change, 2))

        # Commit transaction
        db_helper.commit()

    except (ValueError, RuntimeError, TypeError, AttributeError, KeyError):

        # Rollback transaction
        db_helper.rollback()

        abort(400, description="Something wen't wrong! Try again!")

    # Clean session purchase info
    session["purchase"] = []

    return jsonify({"success_message": success_message})

@app.route("/send_register_products_form")
def send_register_products_form():
    """ Render register_products.html and return as response """

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Get all user products from 'temp_register_list' table
    all_products_from_temp_register_list = db_helper.query_all_products_from_temp_register_list()

    # Create Flask-WTF form to register product
    form = registerProductForm()
    form.categories.choices = [(category["id"], category["category"]) for category in CATEGORIES]

    # Render 'register_products_form.html' and return as response
    return jsonify({"register_products_html": render_template("products_and_services_templates/register_products_form.html", form=form, all_products_from_temp_register_list=all_products_from_temp_register_list)})

@app.route("/send_register_service_form", methods=["POST"])
def send_register_service_form():
    """ Render register_service.html and return """

    form = registerServiceForm()
    
    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # User products
    products = db_helper.query_all_products()

    # Create choices with products description
    choices = [(product["id"], product["description"]) for product in products]

    # Update products field choices 
    for item in form.products_associated:
        item.form.product.choices = choices 

    # Render 'register_services.html'
    return jsonify({"register_service_html": render_template("products_and_services_templates/register_services_form.html", form=form)})

@app.route("/send_edit_product_form", methods=["POST"])
def send_edit_product_form():
    """ Render edit_product_form.html and return """

    # Product id
    product_id = request.data.decode("utf-8")

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Query product information
    product = db_helper.query_product(product_id)
    product = product[0]
    
    # Create Flask-WTF register product form 
    form = registerProductForm()

    # Get product CATEGORY sub categories
    sub_categories = CATEGORIES[product["category"] - 1001]["sub_categories"]

    # Create form categories and sub categories choices
    form.categories.choices = [(category["id"], category["category"]) for category in CATEGORIES]
    form.sub_categories.choices = [(sub_category["sub_category_id"], sub_category["sub_category"]) for sub_category in sub_categories]

    # Set default values for select inputs
    form.unity_m.default = product["unity_m"]
    form.categories.default = product["category"]
    form.sub_categories.default = product["sub_category"]

    # Process form to insert categories and sub categories default
    form.process()

    # Render edit_product_form.html with product information
    edit_product_form_html = render_template("/products_and_services_templates/edit_product_form.html", product_id=product_id, product=product, unity_measurement=UNITY_MEASUREMENT, categories=CATEGORIES[:-1], sub_categories=sub_categories, form=form)

    return jsonify({"edit_product_form_html": edit_product_form_html})

@app.route("/send_edit_service_form_rendered", methods=["POST"])
def send_edit_service_form():
    """ Render edit_service_form.html and return """

    # Product id
    service_id = request.data.decode("utf-8")

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Query service_information information
    service = db_helper.query_service(service_id)

    if not service:
        abort(400, description="Service not registered!")

    service = service[0]

    form = registerServiceForm()

    # Query service products and stocks
    service_products_and_stocks = db_helper.query_service_products(service_id)
    print(service_products_and_stocks)

    # Query all company products basic information
    products = db_helper.query_all_products()

     # Create choices with products description
    choices = [(product["id"], product["description"]) for product in products]

    # Update products field choices 
    for item in form.products_associated:
        item.form.product.choices = choices 

    # Render edit_product_form.html with product information
    edit_service_form_html = render_template("/products_and_services_templates/edit_service_form.html", service_id=service_id, service=service, service_products_and_stocks=service_products_and_stocks, form=form)

    return jsonify({"edit_service_form_html": edit_service_form_html, "service_products_and_stocks": service_products_and_stocks})

@app.route("/send_register_worker_form", methods=["POST"])
def send_register_worker_form():
    """ Render register_worker_form.html and return """

    # Create Flask-WTF register worker form
    form = registerWorkerForm()

    # Configure form select choices
    form.workload_day.choices = [1,2,3,4,5,6,7,8,9,10]
    form.workload_week.choices = [i for i in range(1, 41)]
    form.section.choices = [section for section in SECTIONS]
    form.role.choices = ["Manager", "Chief", "Sub chief", "Worker"]

    # Actual date
    today = date.today()

    # Year
    year = timedelta(days=365)

    # Maximum worker born date - Maximum age to work - 18 years old
    maximum_worker_born_date = today - year * 18

    return jsonify({"register_worker_form": render_template("/human_resources_templates/register_worker_form.html", form=form, maximum_worker_born_date=maximum_worker_born_date)})

@app.route("/send_edit_worker_form", methods=["POST"])
def send_edit_worker_form():
    """ Send as response rendered edit_worker_form.html """

    # Worker id
    worker_id = request.data.decode("utf-8")

    # Initiate Database helper object
    db_helper = current_user.db_connection

    # Query worker
    worker = db_helper.query_worker(worker_id)

    # Ensure worker is registered
    if not worker:
        abort(400, description="Worker not registered!")

    worker = worker[0]

    print(worker)

    # Create Flask-WTF register worker form
    form = registerWorkerForm()

    # Configure form select choices
    form.workload_day.choices = [1,2,3,4,5,6,7,8,9,10]
    form.workload_week.choices = [i for i in range(1, 41)]
    form.section.choices = [section for section in SECTIONS]
    form.role.choices = ["Manager", "Chief", "Sub chief", "Worker"]

    # Set selected input default values with worker info
    form.workload_day.default = str(worker["workload_day"])
    form.workload_week.default = str(worker["workload_week"])
    form.section.default = worker["section"]
    form.role.default = worker["role"]

    form.process()

    # Actual date
    today = date.today()

    # Year
    year = timedelta(days=365)

    # Maximum worker born date - Maximum age to work - 18 years old
    maximum_worker_born_date = today - year * 18

    # Return edit_worker_form_html rendered
    return jsonify({"edit_worker_form": render_template("/human_resources_templates/edit_worker_form.html", form=form, maximum_worker_born_date=maximum_worker_born_date, worker=worker)
})

@app.route("/send_absence_form", methods=["POST"])
def send_absence_form():
    """ Send abstence form with worker abstence infos """
    
    # Worker id sent in request
    worker_id = request.data.decode("utf-8")

    if worker_id == "" or worker_id.isspace():
        abort(400, description="Something wen't wrong!")

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Ensure worker is registered
    worker = db_helper.query_worker(worker_id)

    if not worker:
        abort(400, description="Worker not registered!")

    # Query worker abstences
    worker_absences = db_helper.query_worker_absences(worker_id)

    print(worker_absences)

    # Clean list to append worker abstences years and abstence months
    absences_months_and_years = []

    # Ensure worker has absences and append worker absences years and months if not equal
    if worker_absences:
        for absence in worker_absences:
            # Split month and year from absence date
            start_year, start_month, _ = absence["start_date"].split("-")

            # Append absences month and year 
            absence_month_and_year = f"{start_year}/{start_month}"
             
            if absence_month_and_year not in absences_months_and_years:
                absences_months_and_years.append(absence_month_and_year)

            end_year, end_month, _ = absence["start_date"].split("-")

            # Append absences month and year 
            absence_month_and_year = f"{end_year}/{end_month}"

            if absence_month_and_year not in absences_months_and_years:
                absences_months_and_years.append(absence_month_and_year)

    # Create Flask-WTF register absence form
    register_absence_form = registerAbsenceForm()

    # Create Flask-WTF consult absences form
    consult_absences_form = consultAbsencesForm()

    # Configure consult absence form choices
    consult_absences_form.consult_dates.choices = absences_months_and_years

    # Actual date
    today = date.today()

    # Convert today in to datetime object to compare dates
    today = datetime.now()

    # Create a day timedelta object period
    day = timedelta(days=1)

    # Allowed period
    allowed_period = f"<div class='small-size personal-blue-color f-bold'><span class='color-black'>Allowed date period to register or delete absences:</span> Between {today.date() - (day * 15)} and {today.date()}.</div>"

    # Render abstence_form.html
    abstence_form = render_template("/human_resources_templates/register_abstence_form.html", register_absence_form=register_absence_form, consult_absences_form=consult_absences_form, allowed_period=allowed_period)

    # Return abstence form
    return jsonify({"abstence_form": abstence_form})

@app.route("/send_benefit_form", methods=["POST"])
def send_benefit_form():
    """ Send rendered register_benefit_form.html """

    # Create Flask-WTF register benefit form
    register_benefit_form = registerBenefitForm()

    # Create Flask-WTF consult benefits form
    consult_benefits_form = consultBenefitsForm()

    # Worker id sent in request
    worker_id = request.data.decode("utf-8")

    if worker_id == "" or worker_id.isspace():
        abort(400, description="Select a valid worker.")

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Query worker abstences
    worker_benefits = db_helper.query_worker_benefits(worker_id)

    # Clean list to append worker abstences years and abstence months
    benefits_months_and_years = []

    # Ensure worker has absences and append worker absences years and months if not equal
    if worker_benefits:
        for w_benefit in worker_benefits:
            # Split year and month from benefit date
            year, month, _ = w_benefit["date"].split("-")

            # Append absences month and year 
            benefit_month_and_year = f"{year}/{month}"
             
            if benefit_month_and_year not in benefits_months_and_years:
                benefits_months_and_years.append(benefit_month_and_year)

    # Configure consult_benefits_form consult dates choices
    consult_benefits_form.consult_dates.choices = benefits_months_and_years

    # Actual date
    today = date.today()

    # Allowed periods to delete benefits
    if today.day > 22:
        # Allowed period begin
        allowed_period_begin = (today.year, today.month, 23)

        # Create datetime object date
        allowed_period_begin = datetime(*allowed_period_begin)

        # Use dateutil.relativedelta library to incremenet a month
        allowed_period_end = allowed_period_begin + relativedelta(months=1)
    else:
        # Allowed period begin
        allowed_period_begin = (today.year, today.month + 1, 22)

        # Create datetime object date
        allowed_period_begin = datetime(*allowed_period_begin)

        # Use dateutil.relativedelta library to decrement a month
        allowed_period_end = allowed_period_begin - relativedelta(months=1)

    # Allowed period
    allowed_period = f"<div class='small-size personal-blue-color f-bold'><span class='color-black'>Allowed date period to delete benefits:</span> Between {allowed_period_begin.date()} and {allowed_period_end.date()}.</div>"
    
    # Render abstence_form.html
    benefit_form = render_template("/human_resources_templates/register_benefit_form.html",register_benefit_form=register_benefit_form, consult_benefits_form=consult_benefits_form, allowed_period=allowed_period)

    # Return abstence form
    return jsonify({"benefit_form": benefit_form})

@app.route("/send_create_inventory_form", methods=["POST"])
def send_create_inventory_form():
    """ Create family products inventory and render create_inventory_form.html """

    form = createInventoryForm()
    form.category.choices = [(category["id"], category["category"]) for category in CATEGORIES]

    # Return create_inventory_form.html rendered
    return jsonify({"create_inventory_form": render_template("/inventories_templates/create_inventory_form.html", form=form)})

@app.route("/send_count_inventory_form", methods=["POST"])
def send_count_inventory_form():
    """ Render count_inventory_form.html and return """

    # Inventory data
    inventory_data = request.get_json()

    # Inventory id
    inventory_id = inventory_data["inventory_id"]

    # Pagination index
    pagination_index = inventory_data["pagination_index"]

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Ensure inventory is registered
    try:
        inventory = db_helper.query_inventory(inventory_id)
    except KeyError:
        abort(400, description="Inventory doesn't exist!")

    # Inventory number
    inventory_number = inventory[0]["inventory_number"]

    # Query inventory products
    inventory_products, count_inventory_products = db_helper.query_inventory_products(inventory_id, pagination_index)

    # Nav pagination number of pages
    number_of_pages = math.ceil(count_inventory_products / 25)

    # Ensure inventory is not empty
    if not inventory_products:
        # Delete inventory
        db_helper.delete_inventory(inventory_id)
        abort(400, description="Inventory is empty and will be automatically deleted!")

    # Render inventory_info.html with inventory_info
    count_inventory_form_html = render_template("/inventories_templates/count_inventory_form.html", inventory_number=inventory_number, products=inventory_products, number_of_pages=number_of_pages, pagination_index=pagination_index + 1)

    # Return rendered inventory_info.html
    return jsonify({"count_inventory_form_html": count_inventory_form_html})

@app.route("/send_finish_inventory_form", methods=["POST"])
def send_finish_inventory_form():
    """ Send finish_inventory_form.html """

    # Inventory data
    inventory_data = request.get_json()

    # Inventory id
    inventory_id = inventory_data["inventory_id"]

    # Pagination index
    pagination_index = inventory_data["pagination_index"]

    print(pagination_index)

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Ensure inventory is registered
    try:
        inventory = db_helper.query_inventory(inventory_id)
    except KeyError:
        abort(400, description="Inventory doesn't exist!")

    # Inventory number
    inventory_number = inventory[0]["inventory_number"]

    # Query products information from products table with product information from inventories_products table
    finish_inventory_products, products_count = db_helper.query_inventory_products(inventory_id, pagination_index)

    print(finish_inventory_products)

    # Number of pages
    number_of_pages = math.ceil(products_count / 25)

    # Query inventory global count diff and total (€)
    global_count_diff_and_total = db_helper.query_inventory_diff_and_total(inventory_id)

    global_diff = global_count_diff_and_total[0]["stock_diff"]
    global_diff_value = global_count_diff_and_total[0]["stock_diff_value"]

    # Render finish_inventory_form.html
    finish_inventory_form_html = render_template("/inventories_templates/finish_inventory_form.html", inventory_number=inventory_number, global_diff=global_diff, global_diff_value=global_diff_value, finish_inventory_products=finish_inventory_products, number_of_pages=number_of_pages, pagination_index=pagination_index + 1)

    return jsonify({"finish_inventory_form_html": finish_inventory_form_html})

@app.route("/render_consult_closed_inventories_form", methods=["POST"])
def send_consult_closed_inventories_form():
    """ Render consult_closed_inventories_form.html and return """

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Query closed inventories
    closed_inventories = db_helper.query_closed_inventories()

    # Inventories dates list for user search
    inventories_date = []

    for inventory in closed_inventories:
        # Inventory date
        inventory_date = f"{inventory['month_created']}/{inventory['year_created']}"
        
        # Ensure inventory date is not already listed, else append
        if inventory_date not in inventories_date:
            inventories_date.append(inventory_date)

    return jsonify({"consult_closed_inventories_form_html": render_template("/inventories_templates/consult_closed_inventories_form.html", inventories_date=inventories_date)})


@app.route("/send_recount_inventory_form", methods=["POST"])
def send_recount_inventory_form():
    """ Render recount_inventory_form.html and return """

    # Inventory data
    inventory_data = request.get_json()

    # Inventory id
    inventory_id = inventory_data["inventory_id"]

    # Pagination index
    pagination_index = inventory_data["pagination_index"]

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Ensure inventory is registered
    try:
        inventory = db_helper.query_inventory(inventory_id)
    except KeyError:
        abort(400, description="Inventory doesn't exist!")

    # Inventory number
    inventory_number = inventory[0]["inventory_number"]

    # Query inventory products
    recount_products, count_recount_products = db_helper.query_recount_inventory_products(inventory_id, pagination_index)

    # Nav pagination number of pages
    number_of_pages = math.ceil(count_recount_products / 25)

    # Ensure inventory is not empty
    if not recount_products:
        # Delete inventory
        db_helper.delete_inventory(inventory_id)
        abort(400, description="Inventory is empty and will be automatically deleted!")

    # Render inventory_info.html with inventory_info
    recount_inventory_form_html = render_template("/inventories_templates/recount_inventory_form.html", inventory_number=inventory_number, products=recount_products, number_of_pages=number_of_pages, pagination_index=pagination_index+1)

    # Return rendered inventory_info.html
    return jsonify({"recount_inventory_form_html": recount_inventory_form_html})

@app.route("/render_open_inventories", methods=["POST"])
def send_open_inventories():
    """ Render open_inventories.html and return template """

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Query open inventories
    open_inventories = db_helper.query_open_inventories()

    # Render open_inventories.html
    open_inventories_html = render_template("/inventories_templates/open_inventories.html", open_inventories=open_inventories)

    # Return rendered open_inventories.html
    return jsonify({"open_inventories_html": open_inventories_html})

@app.route("/send_my_products_and_services_rendered")
def send_my_products_and_services_rendered():

    """ Render 'my_products_and_services.html and return as response """

    # Create Flask-WTF search for products and services form
    form = searchProductsAndServicesForm()

    # Define category choices
    form.category_filter.choices = [(category["id"], category["category"]) for category in CATEGORIES]

    # Render 'products_and_services.html' with all products
    my_products_and_services_html = render_template("products_and_services_templates/my_products_and_services.html", categories=CATEGORIES[:-1], form=form)

    return jsonify({"my_products_and_services_html": my_products_and_services_html})


@app.route("/send_edit_products_and_services_rendered", methods=["POST"])
def send_edit_products_and_services_rendered():
    """ Render edit_products_and_services.html and return """

    form = searchAndEditForm()

    # Return rendered 'edit_products_and_services.html'
    return jsonify({"edit_products_and_services_html": render_template("products_and_services_templates/edit_products_and_services.html", form=form)})

@app.route("/send_products_or_services_edit_search_results", methods=["POST"])
def send_edit_products_and_services_search_results():
    """ Search product or service description or bar code and return results """

    # Get form data
    form_data = request.get_json()

    # Create Flask-WTF search and edit form
    form = searchAndEditForm(form_data=form_data)

    if form.validate_on_submit():
        # Initiate Database_helper object
        db_helper = current_user.db_connection

        # Query edit search
        search_results = db_helper.query_edit_search_results(form.search_field.data)
    else:
        search_results = []

    # Render edit_search_results.html
    return jsonify({"edit_search_results_html": render_template("/products_and_services_templates/edit_search_results.html", search_results=search_results, categories=CATEGORIES)})

@app.route("/search_my_products_and_services", methods=["POST"])
def send_my_products_and_services_search_result():
    """ Search products with filters, render 'my_products_and_services_search_results.html' and send in response """
    
    # Initiate Database_helper object
    db_helper = current_user.db_connection
    
    # Data
    data = request.get_json()

    form = searchProductsAndServicesForm(data=data)
    print(data)
    print(form.sub_category_filter.data)

    # Ensure user searched for services
    if form.type_filter.data == "service":
        form.category_filter.choices = ["undefined"]
        form.category_filter.data = "undefined"
    
    else:
        try:
            # Create categories and sub categories filters for search with selected data 
            form.category_filter.choices = [(category["id"], category["category"]) for category in CATEGORIES]
        except TypeError:
            abort(400, description="Complete the fields.")

    # Ensure form is valid
    if form.validate_on_submit():
        # Pagination index
        pagination_index = int(data["pagination_index"])

        # Type filter
        type_filter = data["type_filter"]

        number_of_pages = 0

        # Ensure which type of product user want to search. If product, service or both
        if type_filter == "product":
            # Create sub categories filters for search with selected data 
            sub_categories_filter = [CATEGORIES[int(form.category_filter.data) - 1001]["sub_categories"][i]["sub_category_id"] for i, field in enumerate(form.sub_category_filter) if field.check_box.data]

            # Search products and get results
            if sub_categories_filter:
                search_results, number_of_products = db_helper.query_search_my_products_with_filters(form.data, pagination_index=pagination_index, sub_categories_filter=sub_categories_filter)
            else:
                search_results, number_of_products = db_helper.query_search_my_products_with_filters(form.data, pagination_index=pagination_index)

            number_of_pages = math.ceil(number_of_products / 50)

        elif type_filter == "service":
            # Search services and get results
            search_results = db_helper.query_search_my_services_with_filters(data)

            number_of_pages = math.ceil(len(search_results) / 50)

            number_of_products = len(search_results)
        else:
            abort(400, description="Please select Product or Service!")

        # Render 'my_products_and_servics_search_results.html' with searched products or services
        rendered_search = render_template("products_and_services_templates/my_products_and_services_search_results.html", categories=CATEGORIES, search_results=search_results, pagination_index=pagination_index + 1, number_of_pages=number_of_pages, number_of_products=number_of_products)

        return jsonify({"rendered_search": rendered_search})
    else:
        # Create HTML with errors
        errors = ""
        for _, error in form.errors.items():
            if isinstance(error[0], str):
                errors += f"<p>{error[0]}</p>"
            else:
                for _, v in error[0].items():
                    errors += f"<p>{v[0]}</p>"

        abort(400, description=errors)


@app.route("/send_sub_categories", methods=["POST"])
def send_sub_categories():
    """ Send CATEGORY sub categories """

    # Data
    data = request.get_json()

    # Category id
    category_id = data["category_id"]

    # Convert to integer
    category_id = int(category_id)

    # Categories
    sub_categories = CATEGORIES[category_id - 1001]["sub_categories"]

    # Sub categories options
    sub_categories_options = "<option selected disabled>Select sub category</option>"

    # sub categories checks
    sub_categories_checks = ""

    # Action
    action = data["action"]

    # Create HTML option or check radio elements with sub categories information
    i = 0
    for sub_category in sub_categories:
        sub_category_description = sub_category["sub_category"]
        sub_category_id = sub_category["sub_category_id"]

        if action == "product_input":
            sub_categories_options += f"<option name='sub_category_option' value='{sub_category_id}'>{sub_category_description}</option>"
        else:
            # CSRF token
            csrf_token = data["csrf_token"]

            # Create flask-WTF checkbox mannually
            sub_categories_checks += f"""
            <input id="sub_category_filter-{i}-csrf_token" name="sub_category_filter-{i}-csrf_token" type="hidden" value="{csrf_token}">
            <table id="sub_category-filter-{i}">
                <tbody>
                    <tr>
                        <th>
                             <label class="form-check-label" for="sub_category_filter-{i}-check_box">{sub_category_description}</label>
                        </th>
                        <td>
                            <input class="form-check-input ms-2 me-2" type="checkbox" value="{sub_category_id}" id="sub_category_filter-{i}-check_box" name="sub_category_filter-{index}-check_box">
                        </td>
                    </tr>
                </tbody>
            </table>
            """

        i += 1

    if action == "product_input":
        data = sub_categories_options
    else:
        data = sub_categories_checks

    # Return sub_categories_options
    return jsonify({"sub_categories_options": data})

@app.route("/send_confirm_register_html", methods=["POST"])
def send_confirm_register_rendered():
    """ Render confirm_register.html and return """

    # Initiate Database_helper object
    db_helper = current_user.db_connection
    
    # Get all user products from 'temp_register_list' table
    all_products_from_temp_register_list = db_helper.query_all_products_from_temp_register_list()

    # Render 'products_list.html' with PRODUCTS list and lenght
    confirm_register_html = render_template("products_and_services_templates/confirm_register.html", all_products_from_temp_register_list=all_products_from_temp_register_list, categories=CATEGORIES)

    return jsonify({"confirm_register_html": confirm_register_html})

@app.route("/send_calculated_service_cost_price", methods=["POST"])
def send_calculated_service_cost_price():
    """ Calculate service cost price and return """

    # Service products and stocks
    form_data = request.get_json()

    form = registerServiceForm(form_data=form_data)

    # Update products associated field entries
    entries = 0
    for k,_ in form_data.items():
        if k.startswith("products_associated"):
            entries += 1

    entries = entries / 3

    form.products_associated.min_entries = entries
    form.products_associated.max_entries = entries

    calculated_service_cost_price = 0

    print(form.products_associated.data)

    db_helper = current_user.db_connection

    for data in form.products_associated.data:
        # Query product financial information
        product_financial_info = db_helper.query_product_financial(data["product"])

        # Product cost price
        cost_price = product_financial_info[0]["cost_price"]

        try:
            calculated_service_cost_price += float(data["stock_associated"]) * cost_price 
        except TypeError:
            pass

    cost_price_message = f"Estimated service cost price based on products associated and respective stock: <span class='f-bold' id='calculated_cost_price'>{currency(calculated_service_cost_price)}</span>"

    return jsonify({"cost_price_message":cost_price_message})

@app.route("/send_product_or_service_stocks_content", methods=["POST"])
def send_product_or_service_stocks_content():
    """ Render stocks content based in action send by user side """

    # Data
    data = request.get_json()

    # Product id
    product_or_service_id = data["product_or_service_id"]

    # Action
    action = data["action"]

    if product_or_service_id == "" or action == "":
        abort(400, description="Complete all fields.")

    # Initialize Database_helper object    
    db_helper = current_user.db_connection

    # Ensure user selected product or service
    request_for = data["request_for"]


    if request_for == "product":

        # Query product information
        product_or_service = db_helper.query_product(product_or_service_id)
        
        if not product_or_service:
            abort(400, description="Product not registered!")

        product_or_service = product_or_service[0]

    else:
        # Query service information
        product_or_service = db_helper.query_service(product_or_service_id)
        
        if not product_or_service:
            abort(400, description="Service not registered!")

        product_or_service = product_or_service[0]

    print(product_or_service)

    # Ensure which action was choose
    if action == "register_waste":

        # Create Flask-WTF register waste form
        form = registerWasteForm()
        
        # Return register_waste.html rendered
        return jsonify({"rendered_register_waste_html": render_template("stocks_manager_templates/register_waste_form.html", form=form, product_or_service=product_or_service)})
    
    elif action == "register_regularization":
        
         # Create Flask-WTF register waste form
        form = registerRegularizationForm()

        # Return register_regularization.html rendered
        return jsonify({"rendered_register_regularization_html": render_template("stocks_manager_templates/register_regularization_form.html", form=form, product_or_service=product_or_service)})
    
    else:  
        
        # Return rendered consult_movements_form.html
        return jsonify({"rendered_consult_movements_form_html": render_template("/stocks_manager_templates/consult_movements_form.html", product_or_service=product_or_service)})


@app.route("/send_rendered_order_table", methods=["POST"])
def send_rendered_order_table():
    """ Render order_list_table.html and return """

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Pagination
    pagination_index = request.data.decode("utf-8")

    # Query order products
    order_products_info = db_helper.query_products_from_order_list_with_pagination(pagination_index)

    # Order products with pagination
    order_products = db_helper.query_all_products_from_order_list()

    # Number of pages rounded to next number
    number_of_pages = math.ceil(len(order_products) / 20)

    print(number_of_pages)

    # Query order total
    order_total = db_helper.query_order_total()

    # Render order_list_table.html
    rendered_order_list_table = render_template("register_order_templates/order_list_table.html", order_products=order_products_info, order_total=order_total, pagination_index=int(pagination_index) + 1, number_of_pages=number_of_pages)

    return jsonify({"order_table_html": rendered_order_list_table}) 

@app.route("/send_product_movements", methods=["POST"])
def send_product_movements():
    """ Render product_movements.html and return """

    # Movements data
    movements_data = request.get_json()

    # Product_id
    product_id = movements_data["product_or_service_id"]

    # Pagination index
    pagination_index = movements_data["pagination_index"]

    # html date
    html_start_date = movements_data["start_date"]

    html_end_date = movements_data["end_date"]

    if html_start_date == "" or html_end_date == "":
        abort(400, description="Complete date fields.")

    # Today date object
    today = datetime.now()

    # Ensure dates are valid
    try:
        # Start date object
        start_year, start_month, start_day = html_start_date.split("-")
        start_date = datetime(int(start_year), int(start_month), int(start_day), 0, 0, 0)

        # End date object
        end_year, end_month, end_day = html_end_date.split("-") 
        end_date = datetime(int(end_year), int(end_month), int(end_day), 0, 0, 0)

    except ValueError:
        abort(400, description="Select valid dates.")

    # Ensure start date is lower than end date
    if start_date > end_date:
        abort(400, description="End date must be equal or higher than start date.")

    if start_date > today or end_date > today:
        abort(400, description="Start date or end date cannot be higher than actual date.")

    db_helper = current_user.db_connection

    # Ensure product is registered
    product = db_helper.query_product(product_id)

    if not product:
        abort(400, description="Product not registered!")

    end_date += relativedelta(hours=23, minutes=59)
    
    all_movements = db_helper.query_product_movements(product_id, start_date, end_date, all_movements=True, pagination_index=pagination_index)

    print(all_movements)

    number_of_pages = math.ceil(len(db_helper.query_product_movements(product_id, start_date, end_date, all_movements=True)) / 25)

    # Return product_movements.html rendered 
    return jsonify({"rendered_movements_html": render_template("/stocks_manager_templates/product_or_service_movements.html", all_movements=all_movements, movements=MOVEMENTS, stock=product[0]["stock"], start_date=movements_data["start_date"], end_date=movements_data["end_date"], pagination_index=int(pagination_index) + 1, number_of_pages=number_of_pages)})

@app.route("/send_service_movements", methods=["POST"])
def send_service_movements():
    """ Render product_movements.html and return """

    # Movements data
    movements_data = request.get_json()

    # Product_id
    service_id = movements_data["product_or_service_id"]

    # Pagination index
    pagination_index = movements_data["pagination_index"]

    # html date
    html_start_date = movements_data["start_date"]

    html_end_date = movements_data["end_date"]

    if html_start_date == "" or html_end_date == "":
        abort(400, description="Complete date fields.")

    # Today date object
    today = datetime.now()

    # Ensure dates are valid
    try:
        # Start date object
        start_year, start_month, start_day = html_start_date.split("-")
        start_date = datetime(int(start_year), int(start_month), int(start_day), 0, 0, 0)

        # End date object
        end_year, end_month, end_day = html_end_date.split("-") 
        end_date = datetime(int(end_year), int(end_month), int(end_day), 0, 0, 0)

    except ValueError:
        abort(400, description="Please select valid dates!")

    # Ensure start date is lower than end date
    if start_date > end_date:
        abort(400, description="End date must be equal or higher than start date!")

    if start_date > today or end_date > today:
        abort(400, description="Start date or end date cannot be higher than actual date!")

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Ensure product is registered
    service_info = db_helper.query_service(service_id)

    if not service_info:
        abort(400, description="Product not registered!")

    print(pagination_index)

    end_date += relativedelta(hours=23, minutes=59)
    
    # Query service movements
    all_movements = db_helper.query_service_movements(service_id, start_date, end_date, all_movements=True, pagination_index=pagination_index)

    # Calculate number of pages
    number_of_pages = math.ceil(len(db_helper.query_service_movements(service_id, html_start_date, html_end_date, all_movements=True)) / 25)

    # Return product_movements.html rendered 
    return jsonify({"rendered_movements_html": render_template("/stocks_manager_templates/product_or_service_movements.html", all_movements=all_movements, movements=MOVEMENTS, stock=0, start_date=movements_data["start_date"], end_date=movements_data["end_date"], pagination_index=int(pagination_index) + 1, number_of_pages=number_of_pages)})
    
@app.route("/send_check_expenses_result", methods=["POST"])
def send_check_expenses_result():
    """ Render check expenses results and send in response """

    # Get form data
    form_data = request.get_json()

    # Create Flask-WTF check expenses form
    form = checkExpensesForm(form_data=form_data)

    # Initiate Database_helper object
    db_helper = current_user.db_connection
    
    # Query user expenses
    user_expenses = db_helper.query_all_expenses()

    # Date to check expense
    check_month_choices = []
    check_year_choices = []

    # Append user expenses to check month and check year lists
    for exp in user_expenses:
        if exp["expense_month"] not in check_month_choices:
            check_month_choices.append(exp["expense_month"])
        if exp["expense_year"] not in check_year_choices:
            check_year_choices.append(exp["expense_year"])

    form.year.choices = check_year_choices
    form.month.choices = check_month_choices

    # Ensure form data is valid
    if form.validate_on_submit():
        # Check month
        check_month = form.month.data
        
        # Check year
        check_year = form.year.data

        # Insert dates
        allowed_editable_dates = get_allowed_insert_or_edit_expense_dates(date.today())

        # Ensure expenses are editables
        editable = False

        for dates in allowed_editable_dates:
            month, year = dates.split("/")
       
            if month == check_month and year == check_year:
                editable = True

        # Query for date expenses
        expenses_data = db_helper.query_date_expenses(check_month, check_year)

        # Expenses types + expense type total
        expenses_type_and_totals = []

        for expense_type in EXPENSE_TYPES:
            expense_type_total = 0
            for data in expenses_data:
                if data["expense_id"] == expense_type["expense_id"]:
                    expense_type_total += data["total"]
            
            # Append type and total to expenses_types_and_totals list
            expenses_type_and_totals.append({"expense_id": expense_type["expense_id"], "expense_type": expense_type["expense_description"], "expense_type_total":expense_type_total})

        # Expense total
        expense_total = calculate_total_expenses(expenses_data)

        print(expenses_type_and_totals)

        print(editable)

        rendered_check_expenses_result = render_template("""/expenses_templates/check_expenses_result.html""", expenses_types_and_totals=expenses_type_and_totals,
                                                        expenses_data=expenses_data, expense_total=expense_total,
                                                        check_month=check_month, check_year=check_year,
                                                        editable=editable)

        return jsonify({"success_response": rendered_check_expenses_result})
    else:
        # Create HTML with errors
        errors = ""
        for _, error in form.errors.items():
            errors += f"<p>{error[0]}</p>"

        abort(400, description=errors)

@app.route("/send_rendered_workers_tables", methods=["POST"])
def send_rendered_workers_tables():
    """ Send rendered workers_tables.html """
    
    # Initiate Database_helper object
    db_helper = current_user.db_connection
    
    # Query all workers
    workers_data = db_helper.query_workers()

    # Workers section and data
    workers_section_data = []
    
    for section in SECTIONS:
        workers = []
        for data in workers_data:
            if data["section"].capitalize() == section:
                # Append worker data to workers list
                workers.append(data)

        # Append section and worker data to workers_section_data  list
        workers_section_data.append({"section": section, "workers": workers})

    
    print(workers_section_data)
            
    # Render workers_tables.html
    rendered_workers_tables = render_template("/human_resources_templates/workers_tables.html", workers_section_data=workers_section_data)

    return jsonify({"rendered_workers_tables": rendered_workers_tables})

@app.route("/send_worker_data", methods=["POST"])
def send_worker_info():
    """ Send worker info """

    # Worker id from request
    worker_id = request.data.decode("utf-8")

    # Inititate Database_helper object
    db_helper = current_user.db_connection

    # Query worker data
    worker_data = db_helper.query_worker(worker_id)

    worker_data = worker_data[0]

    print(worker_data)

    return jsonify({"worker_data": worker_data})


@app.route("/send_absences_consult_results", methods=["POST"])
def send_absences_consult_results():
    """ Send absences consult results """

    # Absences form data
    form_data = request.get_json()

    # Worker id
    worker_id = form_data["id"]

    # Initiate Database_helper
    db_helper = current_user.db_connection

    # Query worker abstences
    worker_absences = db_helper.query_worker_absences(worker_id)

    # Clean list to append worker abstences years and abstence months choices
    absences_months_and_years = []

    # Ensure worker has absences and append worker absences years and months if not equal
    if worker_absences:
        for absence in worker_absences:
            # Split month and year from absence date
            start_year, start_month, _ = absence["start_date"].split("-")

            # Append absences month and year 
            absence_month_and_year = f"{start_year}/{start_month}"
             
            if absence_month_and_year not in absences_months_and_years:
                absences_months_and_years.append(absence_month_and_year)

            end_year, end_month, _ = absence["start_date"].split("-")

            # Append absences month and year 
            absence_month_and_year = f"{end_year}/{end_month}"

            if absence_month_and_year not in absences_months_and_years:
                absences_months_and_years.append(absence_month_and_year)

    # Create Flask-WTF consult absences form
    form = consultAbsencesForm(form_data=form_data)

    # Configure consult dates form choices
    form.consult_dates.choices = absences_months_and_years

    # Ensure form has valid data
    if form.validate_on_submit():

        # Get date to consult selected by user
        date_to_consult = str(form.consult_dates.data)

        # Split year and month from date to consult
        year, month = date_to_consult.split("/")

        # Create a day timedelta object period
        day = relativedelta(days=1)

        # Create start date and end date datetime objects
        absence_start_date = datetime(int(year), int(month), 1)
        absence_end_date = absence_start_date + (relativedelta(months=1) - day)

        # Query worker absences with absences dates
        worker_absences_results = db_helper.query_worker_absences(worker_id, [absence_start_date.date(), absence_end_date.date()])

        # Convert today in to datetime object to compare dates
        today = datetime.now()

        # Ensure if absences start date results are in the 15 days period to be deletable
        for absence in worker_absences_results:
            # Get year, month and day from absence start_date
            start_year, start_month, start_day = absence["start_date"].split("-")

            # Create datetime date object to compare dates   
            absence_start_date = datetime(int(start_year), int(start_month), int(start_day))

            fifteen_days_ago = today - (day * 16)
            
            if absence_start_date > fifteen_days_ago and absence_start_date <= today:
                absence["is_deletable"] = True
            else:
                absence["is_deletable"] = False
            
        # Render worker_absences_consult_results.html
        absences_consult_results = render_template("/human_resources_templates/worker_absences_consult_results.html", worker_absences_results=worker_absences_results)

        # Return rendered worker_absences_consult_results.html
        return jsonify({"absences_consult_results": absences_consult_results})
    else:
        # Create HTML with errors
        errors = ""
        for _, error in form.errors.items():
            errors += f"<p>{error[0]}</p>"

        # Abort request and send errors
        abort(400, description=errors)

@app.route("/send_benefits_consult_results", methods=["POST"])
def send_benefits_consult_results():
    """ Send benefits consult results """

    # Request consult benefits form data
    form_data = request.get_json()

    # Worker id
    worker_id = form_data["id"]

    # Initiate Database_helper
    db_helper = current_user.db_connection

    # Query worker abstences
    worker_benefits = db_helper.query_worker_benefits(worker_id)

    # Create Flask-WTF consult benefits form
    form = consultBenefitsForm(form_data=form_data)

    # Clean list to append worker abstences years and abstence months
    benefits_months_and_years = []

    # Ensure worker has absences and append worker absences years and months if not equal
    if worker_benefits:
        for w_benefit in worker_benefits:
            # Split year and month from benefit date
            year, month, _ = w_benefit["date"].split("-")

            # Append absences month and year 
            benefit_month_and_year = f"{year}/{month}"
             
            if benefit_month_and_year not in benefits_months_and_years:
                benefits_months_and_years.append(benefit_month_and_year)

    # Configure form consult dates choices
    form.consult_dates.choices = benefits_months_and_years

    if form.validate_on_submit():
        # Worker id
        worker_id = form_data["id"]
        date_to_consult = form.consult_dates.data

        # Ensure user selected a valid date
        try:
            # Split year and month from date to consult
            year, month = date_to_consult.split("/")

            # Convert year and month to integers
            year = int(year)
            month = int(month)

            # Create datetime start and end dates
            start_date = datetime(year, month, 1)

            # Get end date
            end_date = start_date + relativedelta(months = 1) - relativedelta(days=1)

        except ValueError:
            abort(500, description="Something wen't wrong!")

        print(date_to_consult)

        # Query worker benefits with absences dates
        worker_benefits_results = db_helper.query_worker_benefits(worker_id, [start_date.date(), end_date.date()])
        
        # Actual date
        today = date.today()

        # Benefits total
        benefits_total = 0

        # Allowed periods to delete benefits
        if today.day > 22:
            # Create datetime object date
            allowed_period_begin = datetime(today.year, today.month, 23)

            # Use dateutil.relativedelta library to incremenet a month
            allowed_period_end = allowed_period_begin + relativedelta(months=1)
        else:
            # Create datetime object date
            allowed_period_begin = datetime(today.year, today.month + 1, 22)

            # Use dateutil.relativedelta library to decrement a month
            allowed_period_end = allowed_period_begin - relativedelta(months=1)

        # Ensure if benefits are in allowed period to delete
        for benefit_result in worker_benefits_results:
            # Split year and month from benefit date
            year, month, day = benefit_result["date"].split("-")

            # Convert year and month to integers
            year = int(year)
            month = int(month)
            day = int(day)

            # Create time object with benefit date
            benefit_date = datetime(year, month, day)

            if benefit_date >= allowed_period_begin or benefit_date <= allowed_period_end:
                benefit_result["is_deletable"] = True
            else:
                benefit_result["is_deletable"] = False

            # Increment benefit total
            benefits_total += benefit_result["total"]

        # Render worker_absences_consult_results.html
        benefits_consult_results = render_template("/human_resources_templates/worker_benefits_consult_results.html", worker_benefits_results=worker_benefits_results, benefits_total=benefits_total)

        # Return rendered worker_absences_consult_results.html
        return jsonify({"benefits_consult_results": benefits_consult_results})
    else:
        # Create HTML with errors
        errors = ""
        for _, error in form.errors.items():
            errors += f"<p>{error[0]}</p>"

        # Abort request and send errors
        abort(400, description=errors)



@app.route("/send_select_products_to_inventory_form", methods=["POST"])
def send_select_products_to_inventory_form():
    """ Render select_products_to_inventory_form.html and send with categories products request by user """
    
    # Categories form data
    form_data = request.get_json()

    print(form_data)

    # Create Flask-WTF create inventory form
    form = createInventoryForm(form_data=form_data)

    # Get sub categories selected
    sub_categories = CATEGORIES[int(form_data["category"]) - 1001]["sub_categories"]

    # Insert sub categories choices in form object
    form.category.choices = [(category["id"], category["category"]) for category in CATEGORIES]
    form.sub_category_filter.choices = [sub_category["sub_category_id"] for sub_category in sub_categories]

    # Ensure form data is valid
    if form.validate_on_submit():
        # Category filter to search
        category_filter = form.category.data

        print(category_filter)

        # Create sub categories filters for search with selected data 
        sub_categories_filter = [CATEGORIES[int(form.category.data) - 1001]["sub_categories"][i]["sub_category_id"] for i, field in enumerate(form.sub_category_filter) if field.check_box.data]

        # Pagination index
        pagination_index = json.loads(form_data["extra_form_data"])["pagination_index"]

        # Create filters to search for products
        filters = {'description_bar_code_filter': '', 
                'type_filter': 'All', 'category_filter': category_filter,
                'order_by_filter': 'description', 'asc_desc_filter': 'asc'}
        
        # Initiate Database_helper object
        db_helper = current_user.db_connection

        if sub_categories_filter:
            # Query categories products and count of products
            products,number_of_products = db_helper.query_search_my_products_with_filters(filters, pagination_index, sub_categories_filter=sub_categories_filter)
        else:
            # Query categories products and count of products
            products,number_of_products = db_helper.query_search_my_products_with_filters(filters, pagination_index)

        # Using ceil to get next integer if result of division is float
        number_of_pages = math.ceil(number_of_products / 50)
        print(number_of_pages)

        # Return rendered select_products_to_inventory_form.html
        return jsonify({"success_response": render_template("/inventories_templates/select_products_to_inventory_form.html", products=products, number_of_pages=number_of_pages, pagination_index=int(pagination_index + 1))})
    else:
        # Create HTML with errors
        errors = ""
        for _, error in form.errors.items():
            errors += f"<p>{error[0]}</p>"

        # Abort request and send errors
        abort(400, description=errors)

@app.route("/send_inventory_info", methods=["POST"])
def send_inventory_info():
    """ Render inventory_info.html and return """

    # Inventory data
    inventory_data = request.get_json()

    # Inventory id
    inventory_id = inventory_data["inventory_id"]

    # Pagination index
    pagination_index = inventory_data["pagination_index"]

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Ensure inventory is registered
    try:
        inventory = db_helper.query_inventory(inventory_id)
    except IndexError:
        abort(400, description="Inventory doesn't exist!")

    # Query inventory products
    inventory_products, count_inventory_products = db_helper.query_inventory_products(inventory_id, pagination_index)

    # Nav pagination number of pages
    number_of_pages = math.ceil(count_inventory_products / 25)

    # Ensure inventory is not empty
    if not inventory_products:
        # Delete inventory
        db_helper.delete_inventory(inventory_id)
        abort(400, description="Inventory is empty and will be automatically deleted!")

    # Render inventory_info.html with inventory_info
    inventory_info_html = render_template("/inventories_templates/inventory_info.html", inventory_number=inventory[0]["inventory_number"], products=inventory_products, number_of_pages=number_of_pages, pagination_index = pagination_index + 1)

    # Return rendered inventory_info.html
    return jsonify({"inventory_info_html":inventory_info_html})

@app.route("/send_products_to_recount", methods=["POST"])
def send_products_to_recount():
    """ Change inventory status and product status in inventories_products table """

    # Inventory id
    inventory_id = request.get_json()["inventory_id"]

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Ensure inventory is registered
    try:
        _ = db_helper.query_inventory(inventory_id)
    except KeyError:
        abort(400, description="Inventory doesn't exist!")

    # Products id
    products_id = request.get_json()["products_ids"]

    # Update status in inventories table
    db_helper.update_inventory_status(inventory_id, "recount")

    # Update product status in inventories products table
    db_helper.update_inventory_products_status(inventory_id, products_id, "recount")

    sucess_html = f"<h8 class='color-black'><span class='personal-color-blue f-bold'>{len(products_id)}</span> products sent to recount with sucess!</h8>"

    return jsonify({"sucess_html": sucess_html})

@app.route("/send_closed_inventories_consult_results", methods=["POST"])
def send_closed_inventories_consult_results():
    """ Query closed inventories consult date results and return """

    # Date to consult
    date_to_consult = request.data.decode("utf-8")

    # Parse month and year to consult
    month_to_consult, year_to_consult = date_to_consult.split("/")

    # Initiate Database_helper object
    db_helper = current_user.db_connection
    
    # Query inventories with same dates
    consult_results = db_helper.query_closed_inventories(month=month_to_consult, year=year_to_consult)

    # Return rendered inventories_consult_results.html
    return jsonify({"closed_inventories_consult_results": render_template("/inventories_templates/inventories_consult_results.html", consult_results=consult_results)})

@app.route("/send_closed_inventory_info", methods=["POST"])
def send_closed_inventory_info():
    """ Query closed inventory results and send """

    # Inventory data
    inventory_data = request.get_json()

    # Inventory id
    inventory_id = inventory_data["inventory_id"]

    # Pagination index
    pagination_index = inventory_data["pagination_index"]

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Query closed inventory
    inventory = db_helper.query_inventory(inventory_id)

    # Closed inventory number
    inventory_number = inventory[0]["inventory_number"]

    # Query products information from products table with product information from inventories_products table
    closed_inventory_products, count_inventory_products = db_helper.query_inventory_products(inventory_id, pagination_index=pagination_index)

    number_of_pages = math.ceil(count_inventory_products / 25)

    print(f"Number of pages {number_of_pages}")

    # Query inventory global count diff and total (€)
    global_count_diff_and_total = db_helper.query_inventory_diff_and_total(inventory_id)

    global_diff = global_count_diff_and_total[0]["stock_diff"]
    global_diff_value = global_count_diff_and_total[0]["stock_diff_value"]

    # Return rendered finish_inventory_form.html
    return jsonify({"closed_inventory_result": render_template("/inventories_templates/closed_inventory_result.html", inventory_number=inventory_number, global_diff=global_diff, global_diff_value=global_diff_value, closed_inventory_products=closed_inventory_products, number_of_pages=number_of_pages, pagination_index=pagination_index + 1)})

@app.route("/send_company_sales_and_wastes_analysis", methods=["POST"])
def send_company_sales_and_wastes_analysis():
    """ Render company_sales_and_wastes_analysis.html and return """

    # Data to create bar chart
    data_to_create_chart = request.get_json()

    # Date type
    date_type = data_to_create_chart["date_option_to_search"]

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Date value
    date_value = data_to_create_chart["date"]

    if date_type != "date_period":
        # Ensure data has no special characters
        for item in data_to_create_chart.values():
            if has_special_characters(item):     
                abort(500, description="Something wrong happened!")
    
    if date_type == "year":
        # Convert date value to integer
        date_value = int(date_value)

        # Create datetime objects with start and end search dates
        try:
            search_start_date = datetime(date_value, 1, 1)
            search_end_date = datetime(date_value, 12, 31)
        except ValueError:
            abort(400, description="Please select a valid date!")

        increment_date_value = relativedelta(months=1)

    elif date_type == "month":
        # Split month and year from date value
        month, year = date_value.split("/")
        
        # Convert to integer
        month = int(month)
        year = int(year)

        # Create datetime objects with start and end search dates
        try:
            search_start_date = datetime(year, month, 1)
            search_end_date = search_start_date + relativedelta(months=1) - relativedelta(days=1)
        except ValueError:
            abort(400, description="Please select a valid date!")

        # Increment value
        increment_date_value = relativedelta(days=1)

    else:
        # Begin date
        search_start_date = date_value["start_date"]

        # End date
        search_end_date = date_value["end_date"]

        # Split year, month and day from begin and end date
        start_year, start_month, start_day = search_start_date.split("-")
        end_year, end_month, end_day = search_end_date.split("-")

        # Create datetime objects with begin and end date to compare dates
        try:
            search_start_date = datetime(int(start_year), int(start_month), int(start_day))
            search_end_date = datetime(int(end_year), int(end_month), int(end_day))
        except ValueError:
            abort(400, description="Please select a valid date!")

        # Ensure search start date is not higher than search end date
        if search_start_date > search_end_date:
            abort(400, description="Start date cant be higher than end date!")

        # Ensure end date is not higher than actual date
        if search_end_date > datetime.now():
            abort(400, description="End date cant be higher than actual date!") 

        # Create a timedelta 15 days object
        fifteen_days = timedelta(days=15)

        # Days difference between begin date and end date
        days_diff = search_end_date - search_start_date 

        # Ensure begin date and end date doesnt have more than 15 days of difference
        if days_diff >= fifteen_days:
            abort(400, description="Please select a date period between 1 and 15 days!")

        # Increment value
        increment_date_value = relativedelta(days=1)
        
    # Copy start_date in to a new variable
    itherate_start_date = search_start_date

    # Empty list to save search dates
    start_dates = []
    end_dates = []
    h_start_dates = []
    h_end_dates = []

    # Append to empty lists start and end dates and homologous start and end dates
    while itherate_start_date <= search_end_date:
        if date_type == "year":
            # Create datetime end date object
            end_date = itherate_start_date + relativedelta(months=1) - relativedelta(days=1)
        else:
            end_date = itherate_start_date
        
        # Homlogous start date
        h_start_date = itherate_start_date - relativedelta(years=1)

        # Homologous end date
        h_end_date = end_date - relativedelta(years=1)
        
        # Append start, end and homologous dates
        start_dates.append(itherate_start_date.strftime('%Y-%m-%d'))
        end_dates.append(end_date.strftime('%Y-%m-%d'))
        h_start_dates.append(h_start_date.strftime('%Y-%m-%d'))
        h_end_dates.append(h_end_date.strftime('%Y-%m-%d'))

        # Increment date value to start date
        itherate_start_date += increment_date_value

    # Month sales and wastes empty lists
    sales = []
    wastes = []

    # Homologous month sales and wastes empty_lists
    h_sales = []
    h_wastes = []

    for i,_ in enumerate(start_dates):
        company_sales = db_helper.query_company_sales(start_dates[i], end_dates[i])
        company_wastes = db_helper.query_company_wastes(start_dates[i], end_dates[i])

        # Query homologous sales and wastes
        h_company_sales = db_helper.query_company_sales(h_start_dates[i], h_end_dates[i])
        h_company_wastes = db_helper.query_company_wastes(h_start_dates[i], h_end_dates[i])

        # Append searched company sales and wastes values
        sales.append(company_sales)
        wastes.append(company_wastes)

        # Append homologous company sales and wastes values
        h_sales.append(h_company_sales)
        h_wastes.append(h_company_wastes)
 
    if sum(sales) == 0 and sum(wastes) == 0:
        abort(400, description="No sales and wastes information in this date period!")

    # One hours timedelta object
    one_hour = relativedelta(hours=1)
   
    # Create random date with open and close store time
    random_open_store_date = datetime(2024, 1, 1, 0, 0)
    random_close_store_date = datetime(2024, 1, 1, 23, 59)

    # Hours diff
    hours_diff = 24

    # Three intervals
    interval_hours = math.ceil(hours_diff / 4)

    # Hours labels
    interval_time_sales_labels = []
    
    # Sales data
    interval_time_sales = []

    # Get homologous search dates 
    h_search_start_date = search_start_date - relativedelta(years=1)
    h_search_end_date = search_end_date - relativedelta(years=1)

    # Convert search dates in to strings
    search_start_date = search_start_date.strftime('%Y-%m-%d')
    search_end_date = search_end_date.strftime('%Y-%m-%d')

    h_search_start_date = h_search_start_date.strftime('%Y-%m-%d')
    h_search_end_date = h_search_end_date.strftime('%Y-%m-%d')

    # Get interval time labels
    while random_open_store_date < random_close_store_date:
        # Calculate two hours interval time 
        time_interval_date = random_open_store_date + one_hour * interval_hours

        # If bigger than close store time, set time to close store time
        if time_interval_date > random_close_store_date:
            time_interval_date = random_close_store_date

        # Get hours and minuts string time interval
        head_time = random_open_store_date.strftime("%H:%M")
        end_interval_time = time_interval_date.strftime("%H:%M")
        
        # Append string with time interval
        interval_time_sales_labels.append(f"{head_time}-{end_interval_time}")

        # Query two hours sales values from products_movements table
        sales_total = db_helper.query_company_sales_movement_total(head_time, end_interval_time, search_start_date, search_end_date) 

        # Append 0 to hours_sales_data list index to 0
        interval_time_sales.append(sales_total)

        # Set new head time interval
        random_open_store_date = time_interval_date

    # Sales by interval time labels and values
    interval_time_sales_data = {"interval_time_sales_labels": interval_time_sales_labels, "interval_time_sales": interval_time_sales, "chart_title": "Sales by hours interval"}

    if date_type == "year":
        labels = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    else:
        labels = start_dates

    # Information to create chart with sales and wastes
    sales_and_wastes_data = {"labels": labels, "wastes": wastes, "sales": sales, "chart_title": f"Sales and wastes {search_start_date} - {search_end_date}"}

    # Empty list to save values
    products_units_sell = []
    products_description = []

    # Top 10 products with most units sell
    products_with_most_units_sell = db_helper.query_products_with_most_units_sell(search_start_date, search_end_date)

    # Itherate products description and units sell and append to units_sell and products_description lists
    for product_and_units_sell in products_with_most_units_sell:
        products_units_sell.append(product_and_units_sell["units_sell"])
        products_description.append(product_and_units_sell["product_description"])

    products_units_sell_data = {"products_units_sell": products_units_sell, "products_description": products_description, "bar_color": "#06BFFF"}

    # Empty list to save values
    services_units_sell = []
    services_description = []

    # Top 10 services with most units sell
    services_with_most_units_sell = db_helper.query_services_with_most_units_sell(search_start_date, search_end_date)

    # Itherate products description and units sell and append to units_sell and products_description lists
    for service_and_units_sell in services_with_most_units_sell:
        services_units_sell.append(service_and_units_sell["units_sell"])
        services_description.append(service_and_units_sell["service_description"])

    services_units_sell_data = {"services_units_sell": services_units_sell, "services_description": services_description, "bar_color": "#06BFFF"}

    # Query waste motives and respective values
    waste_motives_and_values = db_helper.query_company_waste_motives_and_values(search_start_date, search_end_date)

    # Motives labels
    motives_labels = []
    
    # Empty list to save waste motive and values
    motives_values = []

    for info in waste_motives_and_values:
        motives_values.append(info["total"])
        try:
            motives_labels.append(WASTE_MOTIVES[201 - info["motive"]]["waste_description"])
        except TypeError:
            if info["motive"] != "" or info["motive"].isspace():
                motives_labels.append(info["motive"])

    # Waste motives labels and values    
    wastes_motives_data = {"motives": motives_labels, "wastes_values": motives_values, "bar_colors": ["brown", "orange", "red", "yellow"]}
        
    # Sum months and sales wastes
    total_sales = sum(sales)
    total_wastes = sum(wastes)

    # Homologous date sales and wastes sums
    h_total_sales = sum(h_sales)
    h_total_wastes = sum(h_wastes)

    # Search date waste diference percentual over sales
    if total_sales > 0 and total_wastes > 0:
        
        waste_percentage = (total_sales - total_wastes) / total_sales * 100
    else:
        waste_percentage = 0

    print(waste_percentage)
    # Calculate sales growth in relation with homologous period
    if h_total_sales > 0 and total_sales > 0:
        sales_growth_percentage = (total_sales - h_total_sales) / total_sales * 100
    else:
        sales_growth_percentage = 0

    if h_total_sales > 0 and h_total_wastes > 0:
        # Homologous waste diference percentual over homologous sales
        h_waste_percentage = h_total_wastes * 100 / h_total_sales
    else:
        h_waste_percentage = 0

    # Query most profit product total and id
    most_profit_product = db_helper.query_most_profit_product(search_start_date, search_end_date)

    if most_profit_product and most_profit_product[0]["product_profit"] > 0:
        # Most profit product profit
        most_profit_product_profit_value = most_profit_product[0]["product_profit"]
            
        # Most profit product description
        most_profit_product_description = most_profit_product[0]["product_description"]
    else:
        most_profit_product_profit_value = 0
        most_profit_product_description = "--"

    # Query most wasted product total and id
    most_wasted_product = db_helper.query_most_wasted_product(search_start_date, search_end_date)

    if most_wasted_product:
        # Most wasted product waste total
        most_wasted_product_waste_value = most_wasted_product[0]["waste"]

        # Most wasted service description
        most_wasted_product_description = most_wasted_product[0]["product_description"]

        if most_wasted_product_waste_value <= 0:
            most_wasted_product_waste_value = 0
            most_wasted_product_description = "--"

    else:
        most_wasted_product_waste_value = 0
        most_wasted_product_description = "--"

    # Query most profit product total and id
    most_profit_service = db_helper.query_most_profit_service(search_start_date, search_end_date)
    
    # Ensure most profit service exist
    if most_profit_service:
        # Most profit service profit
        most_profit_service_profit_value = most_profit_service[0]["service_profit"]
            
        # Most profit service description
        most_profit_service_description = most_profit_service[0]["service_description"]
    else:
        most_profit_service_profit_value = 0
        most_profit_service_description = "--"

    # Query most wasted product total and id
    most_wasted_service = db_helper.query_most_wasted_service(search_start_date, search_end_date)

    # Ensure service exists
    if most_wasted_service:
        # Most wasted product waste total
        most_wasted_service_waste_value = most_wasted_service[0]["waste"]

        # Most wasted product description
        most_wasted_service_description = most_wasted_service[0]["service_description"]
    else:
        most_wasted_service_waste_value = 0
        most_wasted_service_description = "--"

    # Query products benefits
    products_benefits = db_helper.query_products_benefits(search_start_date, search_end_date)

    data_to_render = {
                    "total_sales": total_sales,
                    "total_wastes": total_wastes,
                    "h_total_sales": h_total_sales,
                    "h_total_wastes": h_total_wastes,
                    "sales_growth_percentage": sales_growth_percentage,
                    "waste_percentage": waste_percentage,
                    "h_waste_percentage": h_waste_percentage,
                    "most_profit_product_description": most_profit_product_description,
                    "most_profit_product_profit_value": most_profit_product_profit_value,
                    "most_wasted_product_description": most_wasted_product_description,
                    "most_wasted_product_waste_value": most_wasted_product_waste_value,
                    "most_profit_service_description": most_profit_service_description,
                    "most_profit_service_profit_value": most_profit_service_profit_value,
                    "most_wasted_service_description": most_wasted_service_description,
                    "most_wasted_service_waste_value": most_wasted_service_waste_value,
                    "products_benefits": products_benefits,
                    "search_start_date": search_start_date,
                    "search_end_date": search_end_date,
                    "h_search_start_date": h_search_start_date,
                    "h_search_end_date": h_search_end_date
                    }

    # Render searched_sales_and_wastes.html
    search_sales_and_wastes_rendered = render_template("/sales_and_wastes_analysis_templates/company_searched_sales_and_wastes.html", data_to_render=data_to_render)

    return jsonify({"sales_and_wastes_data": sales_and_wastes_data, "products_units_sell_data": products_units_sell_data, "wastes_motives_data": wastes_motives_data, "interval_time_sales_data": interval_time_sales_data, "services_units_sell_data": services_units_sell_data, "search_sales_and_wastes_rendered": search_sales_and_wastes_rendered})


@app.route("/send_product_sales_and_wastes_analysis", methods=["POST"])
def send_product_sales_and_wastes_analysis():
    """ Render company_sales_and_wastes_analysis.html and return """

    # Data to create bar chart
    data_to_create_chart = request.get_json()

    # Date type
    date_type = data_to_create_chart["date_option_to_search"]

    # Product id
    product_id = data_to_create_chart["product_id"]

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Ensure product exist
    product_info = db_helper.query_product(product_id)

    if not product_info:
        abort(400, description="Product not registered!")

    # Date value
    date_value = data_to_create_chart["date"]

    if date_type != "date_period":
        # Ensure data has no special characters
        for item in data_to_create_chart.values():
            if has_special_characters(item):     
                abort(500, description="Something wrong happened!")
    
    if date_type == "year":
        # Convert date value to integer
        date_value = int(date_value)

        # Ensure user selected a valid date
        try:
            # Create datetime objects with start and end search dates
            search_start_date = datetime(date_value, 1, 1)
            search_end_date = datetime(date_value, 12, 31)
        except ValueError:
            abort(400, description="Please select a valid date!")

        increment_date_value = relativedelta(months=1)

    elif date_type == "month":
        # Split month and year from date value
        month, year = date_value.split("/")
        
        # Convert to integer
        month = int(month)
        year = int(year)

        # Ensure user selected valid dates
        try:
            # Create datetime objects with start and end search dates
            search_start_date = datetime(year, month, 1)
            search_end_date = search_start_date + relativedelta(months=1) - relativedelta(days=1)
        except ValueError:
            abort(400, description="Please select a valid date!")

        # Increment value
        increment_date_value = relativedelta(days=1)

    else:
        # Begin date
        search_start_date = date_value["start_date"]

        # End date
        search_end_date = date_value["end_date"]

        # Split year, month and day from begin and end date
        start_year, start_month, start_day = search_start_date.split("-")
        end_year, end_month, end_day = search_end_date.split("-")

        # Ensure user selected valid dates
        try:
            # Create datetime objects with begin and end date to compare dates
            search_start_date = datetime(int(start_year), int(start_month), int(start_day))
            search_end_date = datetime(int(end_year), int(end_month), int(end_day))
        except ValueError:
            abort(400, description="Please select a valid date!")

        # Ensure search start date is not higher than search end date
        if search_start_date > search_end_date:
            abort(400, description="Start date cant be higher than end date!")

        # Ensure end date is not higher than actual date
        if search_end_date > datetime.now():
            abort(400, description="End date cant be higher than actual date!") 

        # Create a timedelta 15 days object
        fifteen_days = timedelta(days=15)

        # Days difference between begin date and end date
        days_diff = search_end_date - search_start_date 

        # Ensure begin date and end date doesnt have more than 15 days of difference
        if days_diff >= fifteen_days:
            abort(400, description="Please select a date period between 1 and 15 days!")

        # Increment value
        increment_date_value = relativedelta(days=1)
        
    # Copy start_date in to a new variable
    itherate_start_date = search_start_date

    # Empty list to save search dates
    start_dates = []
    end_dates = []
    h_start_dates = []
    h_end_dates = []

    # Append to empty lists start and end dates and homologous start and end dates
    while itherate_start_date <= search_end_date:
        if date_type == "year":
            # Create datetime end date object
            end_date = itherate_start_date + relativedelta(months=1) - relativedelta(days=1)
        else:
            end_date = itherate_start_date
        
        # Homlogous start date
        h_start_date = itherate_start_date - relativedelta(years=1)

        # Homologous end date
        h_end_date = end_date - relativedelta(years=1)
        
        # Append start, end and homologous dates
        start_dates.append(itherate_start_date.strftime('%Y-%m-%d'))
        end_dates.append(end_date.strftime('%Y-%m-%d'))
        h_start_dates.append(h_start_date.strftime('%Y-%m-%d'))
        h_end_dates.append(h_end_date.strftime('%Y-%m-%d'))

        # Increment date value to start date
        itherate_start_date += increment_date_value

    # Month sales and wastes empty lists
    sales = []
    wastes = []

    # Homologous month sales and wastes empty_lists
    h_sales = []
    h_wastes = []

    for i,_ in enumerate(start_dates):
        product_sales = db_helper.query_product_sales(start_dates[i], end_dates[i], product_id)
        product_wastes = db_helper.query_product_wastes(start_dates[i], end_dates[i], product_id)

        # Query homologous sales and wastes
        h_product_sales = db_helper.query_product_sales(h_start_dates[i], h_end_dates[i], product_id)
        h_product_wastes = db_helper.query_product_wastes(h_start_dates[i], h_end_dates[i], product_id)

        # Append searched company sales and wastes values
        sales.append(product_sales)
        wastes.append(product_wastes)

        # Append homologous company sales and wastes values
        h_sales.append(h_product_sales)
        h_wastes.append(h_product_wastes)
    
    if sum(sales) == 0 and sum(wastes) == 0:
        abort(400, description="No sales and wastes information in this date period")    

    # One hours timedelta object
    one_hour = relativedelta(hours=1)
 
    # Create random date with open and close store time
    random_open_store_date = datetime(2024, 1, 1, 0, 0)
    random_close_store_date = datetime(2024, 1, 1, 23, 59)

    # Hours diff
    hours_diff = 24

    # Three intervals
    interval_hours = math.ceil(hours_diff / 4)

    # Hours labels
    interval_time_sales_labels = []
    
    # Sales data
    interval_time_sales = []

    # Get homologous search dates 
    h_search_start_date = search_start_date - relativedelta(years=1)
    h_search_end_date = search_end_date - relativedelta(years=1)

    # Convert search dates in to strings
    search_start_date = search_start_date.strftime('%Y-%m-%d')
    search_end_date = search_end_date.strftime('%Y-%m-%d')

    h_search_start_date = h_search_start_date.strftime('%Y-%m-%d')
    h_search_end_date = h_search_end_date.strftime('%Y-%m-%d')


    # Get interval time labels
    while random_open_store_date < random_close_store_date:
        # Calculate two hours interval time 
        time_interval_date = random_open_store_date + one_hour * interval_hours

        if time_interval_date > random_close_store_date:
            time_interval_date = random_close_store_date

        # Get hours and minuts string time interval
        head_time = random_open_store_date.strftime("%H:%M")
        end_interval_time = time_interval_date.strftime("%H:%M")
        
        # Append string with time interval
        interval_time_sales_labels.append(f"{head_time}-{end_interval_time}")

        # Query two hours sales values from products_movements table
        sales_total = db_helper.query_product_sales_movement_total(head_time, end_interval_time, search_start_date, search_end_date, product_id) 

        # Append 0 to hours_sales_data list index to 0
        interval_time_sales.append(sales_total)

        # Set new interval
        random_open_store_date = time_interval_date

    # Sales by interval time labels and values
    interval_time_sales_data = {"interval_time_sales_labels": interval_time_sales_labels, "interval_time_sales": interval_time_sales, "chart_title": "Sales by hours interval"}
    
    if date_type == "year":
        labels = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    else:
        labels = start_dates

    # Information to create chart with sales and wastes
    sales_and_wastes_data = {"labels": labels, "wastes": wastes, "sales": sales, "chart_title": f"Sales and wastes {search_start_date} - {search_end_date}"}

    # Sum months and sales wastes
    total_sales = sum(sales)
    total_wastes = sum(wastes)

    # Homologous date sales and wastes sums
    h_total_sales = sum(h_sales)
    h_total_wastes = sum(h_wastes)

    # Search date waste diference percentual over sales
    if total_sales > 0 and total_wastes > 0:
        waste_percentage = total_wastes * 100 / total_sales
    else:
        waste_percentage = 0

    # Calculate sales growth in relation with homologous period
    if h_total_sales > 0 and total_sales > 0:
        sales_growth_percentage = (total_sales - h_total_sales) / total_sales * 100
    else:
        sales_growth_percentage = 0

    # Homologous waste diference percentual over homologous sales
    if h_total_sales > 0 and h_total_wastes > 0:
        h_waste_percentage = h_total_wastes * 100 / h_total_sales
    else:
        h_waste_percentage = 0

    # Query waste motives and respective values
    waste_motives_and_values = db_helper.query_product_waste_motives_and_values(search_start_date, search_end_date, product_id)

    # Motives 
    motives = []
    
    # Empty list to save waste values
    motives_values = []

    # Itherate waste motives and value
    for info in waste_motives_and_values:
        # Append waste motive total
        motives_values.append(info["total"])

        # Ensure waste motive is not non identified waste
        try:
            # Append identified waste value
            motives.append(WASTE_MOTIVES[201 - info["motive"]]["waste_description"])
        except TypeError:
            # Append non identified waste value 
            motives.append(info["motive"])
            
    # Wastes and motives labels and data
    wastes_motives_data = {"motives": motives, "wastes_values": motives_values, "bar_colors": ["brown", "red", "orange", "yellow"]}

    # Query product profit
    product_profit = db_helper.query_product_profit(search_start_date, search_end_date, product_id)

    # Query product units sell
    product_and_units_sell = db_helper.query_product_units_sell(search_start_date, search_end_date, product_id)

    # Units sell
    units_sell = product_and_units_sell[0]["units_sell"]

    # Product description
    product_description = product_info[0]["description"]

    data_to_render = {"total_sales": total_sales,
                      "total_wastes": total_wastes,
                      "h_total_sales": h_total_sales,
                      "h_total_wastes": h_total_wastes,
                      "sales_growth_percentage": sales_growth_percentage,
                      "waste_percentage": waste_percentage,
                      "h_waste_percentage": h_waste_percentage,
                      "product_description": product_description,
                      "units_sell": units_sell,
                      "product_profit": product_profit,
                      "search_start_date": search_start_date,
                      "search_end_date": search_end_date,
                      "h_search_start_date": h_search_start_date,
                      "h_search_end_date": h_search_end_date
                    }
   
    # Render product_searched_sales_and_wastes.html
    search_sales_and_wastes_rendered = render_template("/sales_and_wastes_analysis_templates/product_searched_sales_and_wastes.html", data_to_render=data_to_render)

    return jsonify({"sales_and_wastes_data": sales_and_wastes_data, "wastes_motives_data": wastes_motives_data, "interval_time_sales_data": interval_time_sales_data,  "search_sales_and_wastes_rendered": search_sales_and_wastes_rendered})

@app.route("/send_service_sales_and_wastes_analysis", methods=["POST"])
def send_service_sales_and_wastes_analysis():
    """ Render service_sales_and_wastes_analysis.html and return """

    # Data to create bar chart
    data_to_create_chart = request.get_json()

    # Date type
    date_type = data_to_create_chart["date_option_to_search"]

    # Product id
    service_id = data_to_create_chart["service_id"]

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Query service info
    service_info = db_helper.query_service(service_id)

    if not service_info:
        abort(400, description="Service not registered!")

    # Date value
    date_value = data_to_create_chart["date"]

    if date_type != "date_period":
        # Ensure data has no special characters
        for item in data_to_create_chart.values():
            if has_special_characters(item):     
                abort(500, description="Something wrong happened!")
    
    if date_type == "year":
        # Convert date value to integer
        date_value = int(date_value)

        # Create datetime objects with start and end search dates
        try:
            search_start_date = datetime(date_value, 1, 1)
            search_end_date = datetime(date_value, 12, 31)
        except ValueError:
            abort(400, description="Please select a valid date!")

        increment_date_value = relativedelta(months=1)

    elif date_type == "month":
        # Split month and year from date value
        month, year = date_value.split("/")
        
        # Convert to integer
        month = int(month)
        year = int(year)

        # Create datetime objects with start and end search dates
        try:
            search_start_date = datetime(year, month, 1)
            search_end_date = search_start_date + relativedelta(months=1) - relativedelta(days=1)
        except ValueError:
            abort(400, description="Please select a valid date!")

        # Increment value
        increment_date_value = relativedelta(days=1)

    else:
        # Begin date
        search_start_date = date_value["start_date"]

        # End date
        search_end_date = date_value["end_date"]

        # Split year, month and day from begin and end date
        start_year, start_month, start_day = search_start_date.split("-")
        end_year, end_month, end_day = search_end_date.split("-")

        # Create datetime objects with begin and end date to compare dates
        try:
            search_start_date = datetime(int(start_year), int(start_month), int(start_day))
            search_end_date = datetime(int(end_year), int(end_month), int(end_day))
        except ValueError:
            abort(400, description="Please select a valid date!")

        # Ensure search start date is not higher than search end date
        if search_start_date > search_end_date:
            abort(400, description="Start date cant be higher than end date!")

        # Ensure end date is not higher than actual date
        if search_end_date > datetime.now():
            abort(400, description="End date cant be higher than actual date!") 

        # Create a timedelta 15 days object
        fifteen_days = timedelta(days=15)

        # Days difference between begin date and end date
        days_diff = search_end_date - search_start_date 

        # Ensure begin date and end date doesnt have more than 15 days of difference
        if days_diff >= fifteen_days:
            abort(400, description="Please select a date period between 1 and 15 days!")

        # Increment value
        increment_date_value = relativedelta(days=1)
        
    # Copy start_date in to a new variable
    itherate_start_date = search_start_date

    # Empty list to save search dates
    start_dates = []
    end_dates = []
    h_start_dates = []
    h_end_dates = []

    # Append to empty lists start and end dates and homologous start and end dates
    while itherate_start_date <= search_end_date:
        if date_type == "year":
            # Create datetime end date object
            end_date = itherate_start_date + relativedelta(months=1) - relativedelta(days=1)
        else:
            end_date = itherate_start_date
        
        # Homlogous start date
        h_start_date = itherate_start_date - relativedelta(years=1)

        # Homologous end date
        h_end_date = end_date - relativedelta(years=1)
        
        # Append start, end and homologous dates
        start_dates.append(itherate_start_date.strftime('%Y-%m-%d'))
        end_dates.append(end_date.strftime('%Y-%m-%d'))
        h_start_dates.append(h_start_date.strftime('%Y-%m-%d'))
        h_end_dates.append(h_end_date.strftime('%Y-%m-%d'))

        # Increment date value to start date
        itherate_start_date += increment_date_value

    # Month sales and wastes empty lists
    sales = []
    wastes = []

    # Homologous month sales and wastes empty_lists
    h_sales = []
    h_wastes = []

    
    for i,_ in enumerate(start_dates):
        service_sales = db_helper.query_service_sales(start_dates[i], end_dates[i], service_id)
        service_wastes = db_helper.query_service_wastes(start_dates[i], end_dates[i], service_id)

        # Query homologous sales and wastes
        h_service_sales = db_helper.query_service_sales(h_start_dates[i], h_end_dates[i], service_id)
        h_service_wastes = db_helper.query_service_wastes(h_start_dates[i], h_end_dates[i], service_id)

        # Append searched service sales and wastes values
        sales.append(service_sales)
        wastes.append(service_wastes)

        # Append homologous service sales and wastes values
        h_sales.append(h_service_sales)
        h_wastes.append(h_service_wastes)

    # Create random date with open and close store time
    random_open_store_date = datetime(2024, 1, 1, 0, 0)
    random_close_store_date = datetime(2024, 1, 1, 23, 59)

    # Hours diff
    hours_diff = 24

    # Three intervals
    interval_hours = math.ceil(hours_diff / 4)

    # Hours labels
    interval_time_sales_labels = []
    
    # Sales data
    interval_time_sales = []

    one_hour = relativedelta(hours=1)

    # Get homologous search dates 
    h_search_start_date = search_start_date - relativedelta(years=1)
    h_search_end_date = search_end_date - relativedelta(years=1)

    # Convert search dates in to strings
    search_start_date = search_start_date.strftime('%Y-%m-%d')
    search_end_date = search_end_date.strftime('%Y-%m-%d')

    h_search_start_date = h_search_start_date.strftime('%Y-%m-%d')
    h_search_end_date = h_search_end_date.strftime('%Y-%m-%d')

    # Get interval time labels
    while random_open_store_date < random_close_store_date:
        # Calculate two hours interval time 
        time_interval_date = random_open_store_date + (one_hour * interval_hours)

        if time_interval_date > random_close_store_date:
            time_interval_date = random_close_store_date

        # Get hours and minuts string time interval
        head_time = random_open_store_date.strftime("%H:%M")
        end_interval_time = time_interval_date.strftime("%H:%M")
        
        # Append string with time interval
        interval_time_sales_labels.append(f"{head_time}-{end_interval_time}")

        # Query two hours sales values from products_movements table
        sales_total = db_helper.query_service_sales_movement_total(head_time, end_interval_time, search_start_date, search_end_date, service_id) 

        # Append sales_total
        interval_time_sales.append(sales_total)

        # Set new interval
        random_open_store_date = time_interval_date

    # Sales by interval time labels and values
    interval_time_sales_data = {"interval_time_sales_labels": interval_time_sales_labels, "interval_time_sales": interval_time_sales, "chart_title": "Sales by hours interval"}
 
    if date_type == "year":
        labels = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    else:
        labels = start_dates

    # Information to create chart with sales and wastes
    sales_and_wastes_data = {"labels": labels, "wastes": wastes, "sales": sales, "chart_title": f"Sales and wastes {search_start_date} - {search_end_date}"}

    # Motives 
    motives_labels = []
        
    # Empty list to save waste motive and values
    motives_values = []

    # Query waste motives and respective values
    waste_motives_and_values = db_helper.query_service_waste_motives_and_values(search_start_date, search_end_date, service_id)

    print(waste_motives_and_values)

    # Itherate waste motives and value
    for info in waste_motives_and_values:
        # Append waste motive total
        motives_values.append(info["total"])

        # Append identified waste value
        motives_labels.append(WASTE_MOTIVES[201 - info["motive"]]["waste_description"])
 
    wastes_motives_data = {"motives": motives_labels, "wastes_values": motives_values, "bar_colors": ["red", "orange", "yellow"]}


    # Sum date sales and wastes
    total_sales = sum(sales)
    total_wastes = sum(wastes)

    # Sum homologous date sales and wastes
    h_total_sales = sum(h_sales)
    h_total_wastes = sum(h_wastes)

    # Search date waste diference percentual over sales
    if total_sales > 0 and total_wastes > 0:
        waste_percentage = (total_sales - total_wastes) / total_sales * 100
    else:
        waste_percentage = 0

    # Calculate sales growth in relation with homologous period
    if h_total_sales > 0 and total_sales > 0:
        sales_growth_percentage = (total_sales - h_total_sales) / total_sales * 100
    else:
        sales_growth_percentage = 0

    if h_total_sales > 0 and h_total_wastes > 0:
        # Homologous waste diference percentual over homologous sales
        h_waste_percentage = (h_total_sales - h_total_wastes) / h_total_sales * 100
    else:
        h_waste_percentage = 0

    # Query service profit
    service_profit = db_helper.query_service_profit(search_start_date, search_end_date, service_id)

    # Query product units sell
    product_and_units_sell = db_helper.query_service_units_sell(search_start_date, search_end_date, service_id)

    units_sell = product_and_units_sell[0]["units_sell"]

    service_description = service_info[0]["description"]

    data_to_render = {"total_sales": total_sales,
                      "total_wastes": total_wastes,
                      "h_total_sales": h_total_sales,
                      "h_total_wastes": h_total_wastes,
                      "sales_growth_percentage": sales_growth_percentage,
                      "waste_percentage": waste_percentage,
                      "h_waste_percentage": h_waste_percentage,
                      "service_description": service_description,
                      "units_sell": units_sell,
                      "service_profit": service_profit,
                      "search_start_date": search_start_date,
                      "search_end_date": search_end_date,
                      "h_start_date": h_search_start_date,
                      "h_end_date": h_search_end_date
                    }

    # Render searched_sales_and_wastes.html
    search_sales_and_wastes_rendered = render_template("/sales_and_wastes_analysis_templates/service_searched_sales_and_wastes.html", data_to_render=data_to_render)

    return jsonify({"sales_and_wastes_data": sales_and_wastes_data, "wastes_motives_data": wastes_motives_data, "interval_time_sales_data": interval_time_sales_data, "search_sales_and_wastes_rendered": search_sales_and_wastes_rendered})

@app.route("/send_products_without_sales_info", methods=["POST"])
def send_products_without_sales_info_rendered():
    """ Render products_without_sales_info.html and return as response """

    # Pagination index
    pagination_index = int(request.data.decode("utf-8"))

    print("PAGE")
    print(pagination_index)
    print(type(pagination_index))

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Today date
    today = date.today()

    # 15 days ago date
    fifteen_days_ago = datetime(today.year, today.month, today.day) - relativedelta(days=15)

    # Query products without sales in last 15 days with pagination
    products_without_sales = db_helper.query_products_without_sales_in_last_fifteen_days(fifteen_days_ago.date(), today, pagination_index=pagination_index)

    all_products_without_sales = db_helper.query_products_without_sales_in_last_fifteen_days(fifteen_days_ago.date(), today)

    number_of_pages = math.ceil(len(all_products_without_sales) / 25)

    print(type(pagination_index))

    # Render products_without_sales.html
    return jsonify({"products_without_sales_html": render_template("index_templates/products_without_sales.html", products_without_sales=products_without_sales, fifteen_days_ago=fifteen_days_ago.date(), today=today, number_of_pages=number_of_pages, pagination_index=pagination_index + 1)})

@app.route("/send_products_stock_info", methods=["POST"])
def send_products_stock_info():
    """ Render products_stock_info.html and return as response """

    # Request data
    data = request.get_json()

    # Pagination index 
    pagination_index = data["pagination_index"]

    # Search type
    search_type = data["search_type"]

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Query products stock info with pagination
    products_stock_info = db_helper.query_products_by_stock(search_type, pagination_index)

    # Query all products stock info
    all_products_stock_info = db_helper.query_products_by_stock(search_type)

    # Number of pages to send
    number_of_pages = math.ceil(len(all_products_stock_info) / 25)

    # Render products_stock_info.html rendered
    return jsonify({"products_stock_info_html": render_template("index_templates/products_stock_info.html", products_stock_info=products_stock_info, number_of_pages=number_of_pages, pagination_index=pagination_index + 1)})

@app.route("/send_index_main_info", methods=["POST"])
def send_index_main_info():
    """ Render index_main_info.html and return as response """
    # Initiate Database Helper object
    db_helper = current_user.db_connection

    # Query company information
    company_info = db_helper.query_company()

    # Company name
    company_name = company_info[0]["name"]

    # Query all products registered
    all_products = db_helper.query_all_products()

    # Query all services registered
    all_services = db_helper.query_services()

    if all_products:
        # Use date module to get actual date
        today = date.today()

        # Create start and end dates with datetime
        start_date = datetime(today.year, today.month, 1)
        end_date = datetime(today.year, today.month, today.day)
            
        # Query company actual month sales
        company_month_sales = db_helper.query_company_sales(start_date, end_date)

        # Query company actual month wastes
        company_month_wastes = db_helper.query_company_wastes(start_date, end_date)

        # Query products with stock at 0
        products_with_null_stock = db_helper.query_products_by_stock("null_stock")

        # Query products with negative stock
        products_with_negative_stock = db_helper.query_products_by_stock("negative_stock")

        # Get date at 15 days ago
        fifteen_days_ago = end_date - relativedelta(days=15)

        # Query products without sales in last 15 days
        products_without_sales = db_helper.query_products_without_sales_in_last_fifteen_days(fifteen_days_ago.date(), date.today())

        print(products_without_sales)

        data_to_render = {"products_registered": len(all_products),
                          "services_registered": len(all_services),
                          "company_month_sales": company_month_sales,
                          "company_month_wastes": company_month_wastes,
                          "null_stock_products": len(products_with_null_stock),
                          "negative_stock_products": len(products_with_negative_stock),
                          "products_without_sales": len(products_without_sales)}
        
    else:    
        data_to_render = {"products_registered": len(all_products),
                          "services_registered": len(all_services)}
        
    
    return jsonify({"index_main_info_html": render_template("index_templates/index_main_info.html", data_to_render=data_to_render, company_name=company_name)})
        
@app.route("/send_pos_payment_menu", methods=["POST"])
def send_pos_payment_menu():
    """ Render pos_payment_menu.html and return as response """

    # Get purchase total
    try:
        purchase_total = 0

        # Get active purchase
        purchase_info = session["purchase"]

        if not purchase_info:
            abort(400, description="<div class='color-black'>Purchase has no <span class='error-message'>registries</span>!</div>")

        # Get purchase total
        for registry in purchase_info:
            purchase_total += registry["registry_total"] 
            
    except KeyError:
        abort(400, description="Purchase has no registries!")
        
    # Render pos_payment_menu.html with purchase total
    return jsonify({"pos_payment_menu_html": render_template("pos_templates/pos_payment_menu.html", purchase_total=purchase_total)})

@app.route("/send_pos_refund_sale_menu", methods=["POST"])
def send_pos_refund_sale_menu():
    """ Send pos_refund_sale_menu.html rendered as response """

    # Pagination index
    pagination_index = int(request.data.decode("utf-8"))

    # Query pos_id
    pos_id = pos_db.execute("SELECT id FROM pos_system WHERE user_id = ?", current_user.id)
    pos_id = pos_id[0]["id"]

    # Request actual day pos sales
    actual_day_pos_all_sales = pos_db.execute("SELECT * FROM pos_sales_records WHERE pos_id = ? AND DATE(datetime) = ?  ORDER BY datetime ASC", pos_id, date.today())

    # Get number of pages
    number_of_pages = math.ceil(len(actual_day_pos_all_sales) / 50)

    # Offset
    offset = pagination_index * 50

    # Request actual day pos sales
    actual_day_pos_sales_with_pagination = pos_db.execute(f"SELECT * FROM pos_sales_records WHERE pos_id = ? AND DATE(datetime) = ? ORDER BY datetime ASC LIMIT 50 OFFSET {offset}", pos_id, date.today())

    # Render pos_payment_menu.html with purchase total
    return jsonify({"pos_refund_sale_menu_html": render_template("pos_templates/pos_refund_sale_menu.html", actual_day_pos_sales_with_pagination=actual_day_pos_sales_with_pagination, number_of_pages=number_of_pages, pagination_index=pagination_index+1)})

@app.route("/send_pos_sale_info_to_refund", methods=["POST"])
def send_pos_sale_info_to_refund():
    """ Render pos_sale_to_refund.html with POS sale info and return as response """

    # Sale id
    sale_id = request.data.decode("utf-8")

    # Escape special characters
    sale_id = escape(sale_id)

    # Requet sale information
    sale = pos_db.execute("SELECT sales_data, total FROM pos_sales_records WHERE id = ?", sale_id)

    sale_info = json.loads(sale[0]["sales_data"])
    total = sale[0]["total"]

    print(sale_info)

    # Return pos_purchase_info.html rendered with sale information
    return jsonify({"sale_info_to_refund_html": render_template("pos_templates/pos_sale_to_refund.html", sale_info=sale_info, total=total)})

@app.route("/send_pos_sales_and_clients", methods=["POST"])
def send_pos_sales_and_clients():
    """ Query sales and clients from pos_sales_records table and return as response """

    # Query pos_id
    pos_id = pos_db.execute("SELECT id FROM pos_system WHERE user_id = ?", current_user.id)

    # Get sales from open store datetime till now
    sales_info = pos_db.execute("SELECT IFNULL(SUM(total),0) AS sales, COUNT(id) AS clients from pos_sales_records WHERE datetime BETWEEN ? AND ? AND pos_id = ?", session["store_open_datetime"], datetime.now(), pos_id[0]["id"])
    
    sales = sales_info[0]["sales"]
    clients = sales_info[0]["clients"]

    return jsonify({"sales_and_clients": {"sales": currency(sales), "clients": clients}})


@app.route("/send_mensal_report", methods=["POST"])
def send_mensal_report():
    """ Render mensal_report_result.html with mensal report information """

    # Get date to query information
    search_date = request.data.decode("utf-8")

    # Ensure user select a valid date
    try:
        # Split month and year from search date
        month, year = search_date.split("/")

        # Convert to int
        month = int(month)
        year = int(year)

    except (ValueError, RuntimeError, TypeError, AttributeError, KeyError):
        # Abort function and send Error
        abort(500, description="Something wen't wrong!")

    # Empty dicitonary to save expense and values
    mensal_report_data = {}

    # Company month resume values list
    company_month_resume_values = []

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Create datetime start date
    start_date = datetime(year, month, 1)

    # Get end date with date arithmetic
    end_date = start_date + relativedelta(months=1) - relativedelta(days=1)

    # Query company sales
    company_sales = db_helper.query_company_sales(start_date.date(), end_date.date())

    mensal_report_data["Sales"] = f"<span class='sucess-message f-bold'>{currency(company_sales)}</span>"

    # Query company profit
    company_profit = db_helper.query_company_profit(start_date.date(), end_date.date())

    # Increment company_month_resume_total
    company_month_resume_values.append(company_profit)
    
    mensal_report_data["Products and services margin profit"] = f"<span class='sucess-message f-bold'>{currency(company_profit)}</span>"

    # Query company wastes
    company_wastes = db_helper.query_company_wastes(start_date.date(), end_date.date())

    if company_wastes <= 0:
        # Decrement company_month_resume_total
        company_month_resume_values.append(float(str(company_wastes)[1:]))

        company_wastes_element_class = 'sucess-message'
    else:
        company_wastes_element_class = 'error-message'
        
        company_month_resume_values.append(float(f"-{company_wastes}"))

    mensal_report_data["Waste overall (Wastes - benefits)"] = f"<span class='{company_wastes_element_class} f-bold'>{currency(company_wastes)}</span>"

    # Query expenses
    company_expenses = db_helper.query_date_expenses(month, year)

    print(company_expenses)

    # Save expenses with value 0 by default in expenses_and_values dicitionary
    for expense_type in EXPENSE_TYPES:

        # Get expense description
        expense_description = expense_type["expense_description"]

        has_expense = False

        # Ensure expenses exist
        if company_expenses:
            # Itherate expenses and add values to mensal report data
            for expense in company_expenses:
                if expense_type["expense_id"] == expense["expense_id"]:
                
                    mensal_report_data[expense_description] = f"<span class='error-message f-bold'>{currency(expense['total'])}</span>"

                    # Decrement company_month_resume_total
                    company_month_resume_values.append(expense["total"])

                    has_expense = True

                    break
            
            if not has_expense:
                mensal_report_data[expense_description] = currency(0)
                
        else:
            mensal_report_data[expense_description] = currency(0)

    salaries = 0
    benefits = 0

    # Query company workers
    company_workers = db_helper.query_workers()

    # Ensure company has workers and itherate workers to calculate month salary and benefits
    if company_workers:
        for worker in company_workers:
            # Query worker month absences
            worker_absences = db_helper.query_worker_absences(worker["id"], [start_date.date(), end_date.date()])

            # Ensure worker have absences and itherate worker benefits and decrement in workers salaries 
            if worker_absences:
                for absence in worker_absences:
                    salaries -= absence["total"]

            # Query worker month benefits
            worker_benefits = db_helper.query_worker_benefits(worker["id"], [start_date.date(), end_date.date()])

            # Ensure worker have benefits and itherate worker benefits and increment workers_benefits 
            if worker_benefits:
                for w_benefit in worker_benefits:
                    benefits += w_benefit["total"]

    company_month_resume_values.append(salaries + benefits)

    company_month_resume_total = sum(company_month_resume_values)

    if salaries:
        mensal_report_data["Workers salaries"] = f"<span class='error-message f-bold'>{currency(salaries)}</span>"
    else:
        mensal_report_data["Workers salaries"] = currency(salaries)

    if benefits:
        mensal_report_data["Workers benefits"] = f"<span class='error-message f-bold'>{currency(benefits)}</span>"
    else:
        mensal_report_data["Workers benefits"] = currency(benefits)

    return jsonify({"mensal_report_result_html": render_template("mensal_report_templates/mensal_report_result.html", mensal_report_data=mensal_report_data, expense_types=EXPENSE_TYPES, company_month_resume_total=company_month_resume_total)})

@app.route("/send_pos_scanned_product", methods=["POST"])
def send_pos_scanned_product():
    """ Get scanned bar code sent in request and return product information or error if not found """
    # Bar code sent in request
    bar_code = request.data.decode("utf-8")

    # Search bar code for a match
    bar_code_info_queried = current_user.db_connection.query_scanned_bar_code(bar_code)

    print(bar_code_info_queried)

    return jsonify({"bar_code_info_queried": bar_code_info_queried})

@app.route("/send_change_company_name_form", methods=["POST"])
def send_change_company_name_form():
    """ Return change_company_name_form.html rendered as response """
    # Get change_company_name_form
    form = changeCompanyNameForm()
   
    # Return rendered form
    return jsonify({"change_company_name_form": render_template('change_company_name_form.html', form=form)})

@app.route("/send_change_currency_form", methods=["POST"])
def send_change_currency_form():
    """ Return change_currency_form.html rendered as response """

    # Get change currency form
    form = changeCurrencyForm()
   
    # Return rendered form
    return jsonify({"change_currency_form": render_template('change_currency_form.html', form=form)})

@app.route("/send_change_password_form", methods=["POST"])
def send_change_password_form():
    """ Return change_password_form.html rendered as response """

    # Create Flask-wtf change email form
    form = defineNewPasswordForm()

     # Return rendered form
    return jsonify({"change_password_form": render_template('change_password_form.html', form=form)}) 

@app.route("/send_change_personal_code_form", methods=["POST"])
def send_change_personal_code_form():
    """ Return change_personal_code_form.html rendered as response """

    # Create Flask-wtf change email form
    form = defineNewPersonalCodeForm()

     # Return rendered form
    return jsonify({"change_personal_code_form": render_template('change_personal_code_form.html', form=form)}) 

@app.route("/send_change_email_form", methods=["POST"])
def send_change_email_form():
    """ Return change_email_form.html rendered as response """

    # Create Flask-wtf change email form
    form = changeEmailForm()

     # Return rendered form
    return jsonify({"change_email_form": render_template('change_email_form.html', form=form)})

@app.route("/send_authenticator_options", methods=["POST"])
def send_authenticator_options():
    """ Return authenticator_options.html rendered as response """

    return jsonify({"authenticator_options": render_template("authenticator_options.html")})

@app.route("/send_authenticate_password_form", methods=["POST"])
def send_authenticate_password_form():
    """ Return authenticate_password_form.html as response """

    # Create Flask-WTF authenticate password form
    form = authenticatePasswordForm()

    return jsonify({"authenticate_password_form": render_template("authenticate_password_form.html", form=form)})

@app.route("/send_authenticate_personal_code_form", methods=["POST"])
def send_authenticate_personal_code_form():
    """ Authenticate personal code """

    # Create Flask-WTF authenticate form
    form = authenticatePersonalCodeForm()

    return jsonify({"authenticate_personal_code_form": render_template("authenticate_personal_code_form.html", form=form)})

@app.route("/authenticate_personal_code", methods=["POST"])
def authenticate_personal_code():
    """ Authenticate user personal code """

    # Get form data
    form_data = request.get_json()

    # Create Flask-WTF form to authenticate password
    form = authenticatePersonalCodeForm(form_data=form_data)

    # Ensure form is valid
    if form.validate_on_submit():
        # Query user personal code
        personal_code = db.execute("SELECT personal_code FROM users WHERE id = ?", current_user.id)
        personal_code = personal_code[0]["personal_code"]

        # Ensure personal code is valid
        if not check_password_hash(personal_code, form_data["personal_code"]):
            abort(400, description="Invalid personal code!")
        
        return (jsonify({"success_response": "Authenticated with success!"}))
      
    else:
        # Create HTML with errors
        errors = ""
        for _, error in form.errors.items():
            errors += f"<p>{error[0]}</p>"
        
        # Abort request and send errors
        abort(400, description=errors)


@app.route("/authenticate_password", methods=["POST"])
def authenticate_password():
    """ Authenticate user password """

    # Get form data
    form_data = request.get_json()

    # Create Flask-WTF form to authenticate password
    form = authenticatePasswordForm(form_data=form_data)

    # Ensure form is valid
    if form.validate_on_submit():
        # Ensure password is valid
        if not check_password_hash(current_user.password, form_data["password"]):
            # Abort request and send error
            abort(400, description="Invalid password!")

        return (jsonify({"success_response": "Authenticated with success!"}))
    else:
        # Create HTML with errors
        errors = ""
        for _, error in form.errors.items():
            errors += f"<p>{error[0]}</p>"
        
        # Abort request and send errors
        abort(400, description=errors)


@app.route("/validate_change_company_name", methods=["POST"])
def validate_change_company_name():
    """ Validate company name """

    # Get form data
    form_data = request.get_json()

    # Clean data white spaces
    form_data = clean_form_white_spaces(form_data)

    # Get change_company_name_form
    form = changeCompanyNameForm(form_data=form_data)

    # Ensure form is validated
    if form.validate_on_submit():
        # Update company name
        db.execute("UPDATE companies SET name = ? WHERE user_id = ?", form_data["company_name"], current_user.id)
    else:
        # Create HTML with errors
        errors = ""
        for _, error in form.errors.items():
            errors += f"<p>{error[0]}</p>"

        abort(400, description=errors)

    # Return success message
    return jsonify({"success_response": "Company name changed with success!"})

@app.route("/validate_change_currency", methods=["POST"])
def validate_change_currency():
    """ Validate company name """

    # Get form data
    form_data = request.get_json()

    # Clean data white spaces
    form_data = clean_form_white_spaces(form_data)

    # Get change_company_name_form
    form = changeCurrencyForm(form_data=form_data)

    # Ensure form is validated
    if form.validate_on_submit():
        # Update company name
        db.execute("UPDATE companies SET currency = ? WHERE user_id = ?", form_data["currency"], current_user.id)
    else:
        # Create HTML with errors
        errors = ""
        for _, error in form.errors.items():
            errors += f"<p>{error[0]}</p>"

        abort(400, description=errors)

    # Return success message
    return jsonify({"success_response": "Currency changed with success!"})

@app.route("/validate_change_email", methods=["POST"])
def validate_change_email():
    """ Validate email change """

    # Get form data
    form_data = request.get_json()

    # Clean data white spaces
    form_data = clean_form_white_spaces(form_data)

    # Get change_email_form
    form = changeEmailForm(form_data=form_data)

    # Ensure form is validated
    if form.validate_on_submit():
        # Ensure email is not registered
        if db.execute("SELECT * FROM users WHERE email = ?", form_data["email"]):
            abort(400, description="Email already registered!")

        # Update company name
        db.execute("UPDATE users SET email = ? WHERE id = ?", form_data["email"], current_user.id)
    else:
        # Create HTML with errors
        errors = ""
        for _, error in form.errors.items():
            errors += f"<p>{error[0]}</p>"

        abort(400, description=errors)

    # Return success message
    return jsonify({"success_response": "Email changed with success! You will be redirected to login in 3 seconds.."})

@app.route("/validate_change_password", methods=["POST"])
def validate_change_password():
    """ Validate password change """

    # Get form data
    form_data = request.get_json()

    # Get change_email_form
    form = defineNewPasswordForm(form_data=form_data)

    # Ensure form is validated
    if form.validate_on_submit():
        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(form_data["new_password"]), current_user.id)
    else:
        # Create HTML with errors
        errors = ""
        for _, error in form.errors.items():
            errors += f"<p>{error[0]}</p>"

        abort(400, description=errors)

    # Return success message
    return jsonify({"success_response": "Password changed with success! You will be redirected to login in 3 seconds.."})

@app.route("/validate_change_personal_code", methods=["POST"])
def validate_change_personal_code():
    """ Validate personal code change """

    # Get form data
    form_data = request.get_json()

    # Get change_email_form
    form = defineNewPersonalCodeForm(form_data=form_data)

    # Ensure form is validated
    if form.validate_on_submit():
        db.execute("UPDATE users SET personal_code = ? WHERE id = ?", generate_password_hash(form_data["new_personal_code"]), current_user.id)
    else:
        # Create HTML with errors
        errors = ""
        for _, error in form.errors.items():
            errors += f"<p>{error[0]}</p>"

        abort(400, description=errors)

    # Return success message
    return jsonify({"success_response": "Password changed with success! You will be redirected to login in 3 seconds.."})
   
def validate_service(service_description, products_and_stocks):
    """ Validate service """

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Query all user services
    services = db_helper.query_services_basic()

    # Ensure service is not registered
    for service in services:
        if service["description"] == service_description:
            abort(500, description=f"Service description {service['description']} already registered.")

    for p_and_s in products_and_stocks:
        # Query product
        product = db_helper.query_product(p_and_s["product"])
        
        # Ensure product is registered
        if not product:
            abort(400, description=f"Product {product} not registered")

@app.route("/validate_product_register", methods=["POST"])
def validate_product_and_insert_in_temp_register_list():
    """ Validate product register and insert in temp_register_list table """

    # Get form data
    form_data = request.get_json()

    # Clean form data white spaces
    form_data = clean_form_white_spaces(form_data) 

    # Create Flask-WTF register product form
    form = registerProductForm(form_data=form_data)

    # Ensure user selected categories and sub categories
    try:
        # Get sub categories
        sub_categories = CATEGORIES[int(form.data["categories"]) - 1001]["sub_categories"]

        # Insert categories and sub categories choices in form object
        form.sub_categories.choices = [sub_category["sub_category_id"] for sub_category in sub_categories]
        form.categories.choices = [category["id"] for category in CATEGORIES]
    except TypeError:
        abort(400, description="Complete the fields.")

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Query all products from temp register list
    temp_register_products = db_helper.query_all_products_from_temp_register_list()

    # Ensure list not pass limit of 100 products listed
    if len(temp_register_products) == 100:
        abort(400, description="List reached maximum limit: 100.")
    
    # Ensure form data is valid
    if form.validate_on_submit():
        # Query all company products
        all_products = db_helper.query_all_products()

        print(all_products)

        # Ensure product description or bar code is not already registered
        for product in all_products:
            print(product["bar_code"])
            print(form.bar_code.data.upper())
            if product["description"] == form.product_description.data.upper() or product["bar_code"] == form.bar_code.data.upper():
                abort(400, description="Product description or bar code already registered!")

        # Convert cost price and sell price to float with two decimals
        cost_price = float(round(form.cost_price.data, 2))
        sell_price = float(round(form.sell_price.data, 2))

        if cost_price >= sell_price:
            abort(400, description="Sell price must be higher than cost price!")

        # Get margin percentage
        margin_percentage = calculate_price_margin(cost_price, sell_price)

        print(form.stock.data)

        try:
            # Insert product in temp_register_list table
            db_helper.insert_product_in_temp_register_list(form.product_description.data.upper(), form.bar_code.data.upper(), form.unity_m.data, form.categories.data, form.sub_categories.data, cost_price, sell_price, round(margin_percentage,2), round(float(form.stock.data), 3))      
        except ValueError:
            abort(400, description="Product description or bar code already listed.")
    else:
        # Create HTML with errors
        errors = ""
        for _, error in form.errors.items():
            errors += f"<p>{error[0]}</p>"

        # Abort function and send errors as response
        abort(400, description=errors)

    # Return sucess message to user-side
    return jsonify({"success_response": "Product validated with sucess! To register click on 'Confirm register'!"})

@app.route("/validate_and_edit_product", methods=["POST"])
def validate_and_edit_product():
    """ Validate product edit and save changes """

    # Get form data
    form_data = request.get_json()

    # Clean form data white spaces
    form_data = clean_form_white_spaces(form_data)

    # Create Flask-WTF registerproduct form
    form = registerProductForm(form_data=form_data)

    # Get sub categories
    sub_categories = CATEGORIES[int(form.categories.data) - 1001]["sub_categories"]

    # Define categories and sub categories choices
    form.sub_categories.choices = [(sub_category["sub_category_id"], sub_category["sub_category"]) for sub_category in sub_categories]
    form.categories.choices = [(category["id"], category["category"]) for category in CATEGORIES]

    # Ensure form is valid
    if form.validate_on_submit():
        # Initiate Database_helper object
        db_helper = current_user.db_connection

        # Product id
        product_id = form_data["id"]

        # Query all company products
        all_products = db_helper.query_all_products()

        product_description = form.product_description.data.upper()
        bar_code = form.bar_code.data.upper()
        unity_m = form.unity_m.data

        # Ensure product description or bar code is not already registered
        for product in all_products:
            if product["id"] != int(product_id):
                if product["description"] == product_description or product["bar_code"] == form.bar_code.data.upper():
                    abort(400, description="Product description or bar code already registered!")

        # Convert cost price and sell price to float with two decimals
        cost_price = float(form.cost_price.data)
        sell_price = float(form.sell_price.data)

        if cost_price >= sell_price:
            abort(400, description="Sell price must be higher than cost price!")

        # Query product
        product_registered_information = db_helper.query_product(product_id) 

        # Ensure product is registered
        if not product_registered_information:
            abort(400, description="Product not registered!")
        
        basic_changed = False
        financial_changed = False
        prices_changed = False
        service_afected = False
        
        # Convert category and sub category to int
        category = int(form.categories.data)
        sub_category = int(form.sub_categories.data)

        # Ensure product has changes
        for info in product_registered_information:
            if info["description"] != product_description or info["bar_code"] != bar_code or info["category"] != category or info["sub_category"] != sub_category:  
                # Set basic change to True
                basic_changed = True
            
            if info["cost_price"] != cost_price or info["sell_price"] != sell_price:
                # Set financial change to True
                financial_changed = True

                # Set prices change to True
                prices_changed = True

                if info["cost_price"] != cost_price:
                    service_afected = True

            if info["unity_m"] != unity_m:
                # Set financial change to True
                financial_changed = True
                
        if not basic_changed and not financial_changed and not prices_changed:
            abort(400, description="No changes detected!")
        
        if basic_changed:
            # Update products basic
            db_helper.update_product_basic(product_id, product_description, bar_code, category, sub_category)

        if financial_changed and prices_changed:
            # Calculate new margin percentage
            new_margin_percentage = calculate_price_margin(cost_price, sell_price)

            # Update products financial with new margin_percentage
            db_helper.update_product_financial(product_id, cost_price, sell_price, new_margin_percentage, unity_m)

        if financial_changed and not prices_changed:
            # Update unity of meausrement with same prices and margin percentage
            db_helper.update_product_financial(product_id, cost_price, sell_price, product_registered_information[0]["margin_percentage"], unity_m)

        if service_afected:
            # Ensure product has services associated
            services_associated = db_helper.query_product_services_associated(product_id)
        else:
            services_associated = []

        print(services_associated)

        # Render edit_product_sucess.html
        edit_product_sucess_html = render_template("products_and_services_templates/edit_product_sucess.html", product_description=product_description, services_associated=services_associated)

        return jsonify({"success_response": edit_product_sucess_html})
    
    else:

        # Create HTML with errors
        errors = ""
        for _, error in form.errors.items():
            errors += f"<p>{error[0]}</p>"

        # Abort request and send errors
        abort(400, description=errors)

@app.route("/validate_and_edit_service", methods=["POST"])
def validate_and_edit_service():
    """ Validate service edit and update service tables """

    # Get form data
    form_data = request.get_json()

    # Clean form data white spaces
    form_data = clean_form_white_spaces(form_data)

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Get service id
    service_id = int(form_data["id"])

    # Query service
    service = db_helper.query_service(service_id)

    # Ensure service_id is registered
    if not service:
        abort(400, description="Service not registered!")

    # Create Flask-WTF registerproduct form
    form = registerServiceForm(form_data=form_data)

    # Update products associated field entries
    entries = 0
    for k,v in form_data.items():
        if k.startswith("products_associated"):
            entries += 1

    entries = entries / 3

    form.products_associated.min_entries = entries
    form.products_associated.max_entries = entries

    # User products
    products = db_helper.query_all_products()

    # Create choices with products description
    choices = [(product["id"], product["description"]) for product in products]

    items_values = []

    # Update products field choices 
    for item in form.products_associated:
        if item.form.product.data not in items_values:
            items_values.append(item.form.product.data)

        for i in range(len(choices)):
            if choices[i][0] in items_values:
                choices.pop(i)

        item.form.product.choices = choices

    if form.validate_on_submit():
        # Convert cost price and sell price to float
        service_cost_price = float(form.cost_price.data)
        service_sell_price = float(form.sell_price.data)

        # Ensure cost price is not higher or equal to sell price
        if service_cost_price >= service_sell_price:
            abort(400, description="Sell price must be higher than cost price.")


        # Ensure user changed data
        basic_changed = False
        financial_changed = False
        products_and_stocks_changed = False
        service_description = form.service_description.data
        service_products_and_stocks = form.products_associated.data

        # Ensure services basic has changes
        if service_description != service[0]["description"]:
            basic_changed = True
        
        # Ensure services financial has changes
        if service_cost_price != service[0]["cost_price"] or service_sell_price != service[0]["sell_price"]:
            financial_changed = True

        # Query service products and stocks registered
        registered_service_products_and_stocks = db_helper.query_service_products(service_id)

        # Ensure products and stocks has changes
        for product_and_stock in service_products_and_stocks:
            # Ensure product is registered
            product = db_helper.query_product(product_and_stock["product"])
            if not product:
                abort(400, description="One of the products you want to associate to service is not registered!")

            has_product_stock_changes = False
    
            for registered_product_and_stock in registered_service_products_and_stocks:
                if float(product_and_stock["product"]) == registered_product_and_stock["product_id"] and float(product_and_stock["stock_associated"]) != registered_product_and_stock["stock"]:
                    has_product_stock_changes = True
                    break

            # Ensure product in products and stocks list to edit has changes or product is not registered
            if has_product_stock_changes or len(service_products_and_stocks) != len(registered_service_products_and_stocks):
                products_and_stocks_changed = True

        if not basic_changed and not financial_changed and not products_and_stocks_changed:
            abort(400, description="No changes detected!")

        # Ensure which section was edit in service
        if basic_changed:
            # Update services basic
            db_helper.update_service_basics(service_id, service_description)

        if financial_changed:
            # Calculate new margin percentage
            margin_percentage = calculate_price_margin(service_cost_price, service_sell_price)

            # Update service financial
            db_helper.update_service_financial(service_id, service_cost_price, service_sell_price, margin_percentage)

        if products_and_stocks_changed:
            # Update products and stocks
            db_helper.update_service_products_and_stocks(service_id, service_products_and_stocks)
    else:
        # Create HTML with errors
        errors = ""
        for _, error in form.errors.items():
            print(error)
            if isinstance(error[0], str):
                errors += f"<p>{error[0]}</p>"
            else:
                for _, v in error[0].items():
                    errors += f"<p>{v[0]}</p>"

        abort(400, description=errors)

    # Return sucess html
    return jsonify({"success_response": f"<div class='row mt-3 mb-3'><div class='col-lg-12 mt-3 mb-3'><h5 class='personal-blue-color text-center'>{service_description} edited with sucess!</h5></div>"})

@app.route("/validate_product_and_insert_in_temp_order_list", methods=["POST"])
def validate_product_and_insert_in_temp_order_list():
    """ Validate user input and insert in temp order list """

    # Get form data
    form_data = request.get_json()

    # Product id
    product_id = form_data["id"]

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Query product
    product_info = db_helper.query_product(product_id)

    # Ensure product is registered
    if not product_info:
        abort(400, description="Product not registered.")

    form = registerProductInOrderForm(form_data=form_data)


    if form.validate_on_submit():
        # Get form data 
        product_description = form.description.data
        bar_code = form.bar_code.data
        cost_price = float(form.cost_price.data)
        sell_price = float(form.sell_price.data)
        quantity = float(form.quantity.data)
        
        # Ensure cost price is not equal or higher than sell price
        if cost_price >= sell_price:
            abort(400, description="Sell price must be higher than cost price.")

        # Query all products in temp_order_list table
        order_products = db_helper.query_products_from_order_list_with_pagination()

        if len(order_products) == 100:
            abort(400, description="Maximum products per order reached! Delete some product from order or register in other order!")
        
        # Ensure product is not in list already
        for product in order_products:
            if product_description == product["description"]:
                abort(400, description=f"Product with description {product_description} already in order.")
            if bar_code == product["bar_code"]:
                abort(400, description=f"Product with bar code {bar_code} already in order.")
        
        # Query all user products
        all_products = db_helper.query_all_products()
        
        is_registered = False
        
        # Ensure user insert correct product information if already registered
        for product_info in all_products:
            if product_description == product_info["description"] and bar_code == product_info["bar_code"]:
                is_registered = True
                break

        if not is_registered:
            abort(400, description=f"Product: {product_description} with bar code: {bar_code} is not registered!")
            
        # Insert product in temp order list
        db_helper.insert_products_in_temp_order_list(product_id, product_description, bar_code, cost_price, sell_price, quantity)
        
        # Sucess message
        sucess_message = "Product submited with sucess in order!"
        
        # Return order_list_table.html rendered with order_list updated
        return jsonify({"success_response": sucess_message})
    
    else:
        errors = ""
        for _, error in form.errors.items():
            print(error)
            if isinstance(error[0], str):
                errors += f"<p>{error[0]}</p>"
            else:
                for _, v in error[0].items():
                    errors += f"<p>{v[0]}</p>"

        abort(400, description=errors)
    
@app.route("/validate_order_upload", methods={"POST"})
def validate_order_upload():
    """ Validate order upload """

    # Uploaded file
    try:
        file = request.files['file']
    except KeyError:
        abort(500, description="Please select a file!")

    # Ensure file exists
    if not file:
        abort(500, description="Please select a file!")

    print(file.filename)
    
    # Ensure file is csv
    if not allowed_file(file.filename):
        abort(500, description="Only 'csv' file format allowed!")

    # Ensure file has maximum size of 16MB
    if len(file.read()) > MAX_CONTENT_LENGTH:
        abort(400, descrition="File too large! Maximum file size is 16MB.")
    
    # Return pointer to file begin
    file.seek(0)

    # Convert csv file bytes in to text using StringIO
    file = file.read().decode("utf-8")
    converted_csv_file = StringIO(file)

    # Read csv file with CSVreader
    reader = csv.DictReader(converted_csv_file, delimiter=";")

    # Initiate Database_helper object
    db_helper = current_user.db_connection
    
    # List to collect order data
    order_data = []

    rows = 0

    # Read csvfile and send order information
    for row in reader:
        # Products info
        try:
            description = row["description"]
            bar_code = row["bar_code"]
            cost_price = row["cost_price"]
            sell_price = row["sell_price"]
            quantity = row["quantity"]

            # Escape special characters
            description = escape(description)
            bar_code = escape(bar_code)
            cost_price = escape(cost_price)
            sell_price = escape(sell_price)
            quantity = escape(quantity)

            try:
                cost_price = float(cost_price)
                sell_price = float(sell_price)
            except ValueError:
                abort(400, description="Please insert valid prices!")

            try:
                quantity = int(quantity)
            except ValueError:
                abort(400, description="Please insert valid quantities!")

            # Clean description and bar code white spaces
            description = clean_white_spaces(description)
            bar_code = clean_white_spaces(bar_code)

        except KeyError:
            # Ensure headers are correct
            abort(400, description="Your csv file headers are not correct! Fix them or download our csv file again.")

        if None in [description, bar_code, cost_price, sell_price, quantity]:
            abort(400, description="Your file got errors! Download our file again if you're using Microsoft Excel. If you're using Notepad to edit be sure your values are delimited by semicolons!")

        # Query product id
        product_id = db_helper.query_product_id(description)

        if not product_id:
            abort(400, description=f"Product {description} not registered!")

        # Order data list append produdct data
        order_data.append({"id": str(product_id[0]["id"]), "description": description, "bar_code": bar_code, "cost_price": str(cost_price), "sell_price": str(sell_price), "quantity": str(quantity)})

        # Incremenet rows
        rows += 1

    # Ensure file is not empty
    if rows == 0:
        abort(400, description="File is empty!")

    # Return data as response
    return jsonify({"order_data": order_data, "sucess_message": "Order uploaded with sucess!"})

@app.route("/validate_and_register_expense", methods=["POST"])
def validate_and_register_expense():
    """ Validate and insert expense in expenses table """

    form_data = request.get_json()

    form = registerExpenseForm(form_data=form_data)

    # Actual date
    today = date.today()

    # Default dates    
    if today.day < 23:
        insert_dates = [f"{today.month}/{today.year}", f"{today.month + 1}/{today.year}"]
    else:
        insert_dates = [f"{today.month + 1}/{today.year}", f"{today.month + 2}/{today.year}"]

    # Ensure month is not 11 or 12 
    if today.month == 11 and today.day >= 23 or today.month == 12 and today.day < 23:
        insert_dates[0] = f"{12}/{today.year}"
        insert_dates[1] = f"{1}/{today.year + 1}"
    elif today.month == 12 and today.day >= 23:
        insert_dates[0] = f"{1}/{today.year + 1}"
        insert_dates[1] = f"{2}/{today.year + 1}"

    # Define month and year choices and expenses choices
    form.month_year_dates.choices = insert_dates
    form.expenses.choices = [(expense["expense_id"], expense["expense_description"]) for expense in EXPENSE_TYPES]

    if form.validate_on_submit():
        # Expense type
        expense = form.expenses.data

        # Expense total
        expense_total = float(form.total.data)

        # Expense date
        expense_date = form.month_year_dates.data

        # Split "/" from expense_date and get month and year
        expense_month, expense_year = expense_date.split("/")
    
        # Initiate Database_helper object
        db_helper = current_user.db_connection

        # Get atual date
        today = date.today()
        insert_year = today.year
        insert_month = today.month
        insert_day = today.day

        # Insert expense in expenses table
        db_helper.insert_expense(expense, expense_total, expense_year, expense_month, insert_year, insert_month, insert_day) 

        return jsonify({"success_response": f"Expense: <span class='personal-blue-color'>{EXPENSE_TYPES[int(expense) - 301]['expense_description']}</span> in total: <span class='personal-blue-color f-bold'>{currency(expense_total)}</span> inserted with success!"})
        
    else:
        # Create HTML with errors
        errors = ""
        for _, error in form.errors.items():
            print(error)
            if isinstance(error[0], str):
                errors += f"<p>{error[0]}</p>"
            else:
                for _, v in error[0].items():
                    errors += f"<p>{v[0]}</p>"

        abort(400, description=errors)

@app.route("/validate_worker", methods=["POST"])
def validate_worker_data():
    """ Validate and register worker in workers table """

    # Get form data with cleaned whitespaces
    form_data = clean_form_white_spaces(request.get_json())

    # Create Flask-WTF register worker form
    form = registerWorkerForm(form_data=form_data)

    # Configure form select choices
    form.workload_day.choices = [1,2,3,4,5,6,7,8,9,10]
    form.workload_week.choices = [i for i in range(1, 41)]
    form.section.choices = [section for section in SECTIONS]
    form.role.choices = ["Manager", "Chief", "Sub chief", "Worker"]

     # Ensure workload by day is not higher than workload by week
    if int(form_data["workload_day"]) > int(form_data["workload_week"]):
        abort(400, description="Workload by day can't be higher than workload by week.")

    if form.validate_on_submit():

        # Ensure worker data to validate is for register or edit
        try:
            worker_id = form_data["id"]

            # Initiate Database helper object
            db_helper = current_user.db_connection

            # Query worker
            worker = db_helper.query_worker(worker_id)

            # Ensure worker is registered
            if not worker:
                abort(400, description="Worker not registered!")
            
            worker = worker[0]

            # Convert form data and remove csrf key from form data
            form_data.pop("csrf_token")
            form_data["workload_day"] = int(form_data["workload_day"])
            form_data["workload_week"] = int(form_data["workload_week"])
            form_data["base_salary"] = float(form_data["base_salary"])
            form_data["id"] = int(form_data["id"])

            worker.popitem() # Remove last item from registered worker data

            # Ensure user changed worker data
            if form_data == worker:
                abort(400, description="No changes detected!")

        except KeyError:
            pass

        # Worker born date
        worker_born_date = str(form.born_date.data)

        # Ensure user registered or updated has more than 18years old
        today = date.today()
        
        # Year
        year = relativedelta(years=1)

        # Split year month and day from worker born date
        worker_year, worker_month, worker_day = worker_born_date.split("-")

        # Min age date - 18 years
        min_age_to_work = today - year * 18
        
        # Create datetime objects to compare min age with worker born date
        min_age_to_work = datetime(min_age_to_work.year, min_age_to_work.month, min_age_to_work.day)
        inputed_worker_born_date = datetime(int(worker_year), int(worker_month), int(worker_day))

        # Ensure worker born date is not higher than min age to work born date
        if inputed_worker_born_date > min_age_to_work:
            abort(400, description="Invalid born date! Worker must have a minimum age of 18 years old!")
        
        return jsonify({"cleaned_data": form_data})
    else:
        # Create HTML with errors
        errors = ""
        for _, error in form.errors.items():
            print(error)
            if isinstance(error[0], str):
                errors += f"<p>{error[0]}</p>"
            else:
                for _, v in error[0].items():
                    errors += f"<p>{v[0]}</p>"

        # Abort function and send errors as response
        abort(400, description=errors)


@app.route("/validate_and_register_absence", methods=["POST"])
def validate_and_register_absence():
    """ Validate and register absence in absences table """

    # Absence form data
    form_data = request.get_json()
    
    # Absence worker id
    worker_id = form_data["id"]

    # Initiate Database_helper
    db_helper = current_user.db_connection

    # Query worker
    worker_info = db_helper.query_worker(worker_id)

    # Ensure worker exists
    if not worker_info:
        abort(400, description="Worker not registered!")

    # Create Flask-WTF register absence form
    form = registerAbsenceForm(form_data=form_data)

    # Ensure form data is valid
    if form.validate_on_submit():

        # Absence start date
        absence_start_date = form.start_date.data
        # Absence end date
        absence_end_date = form.end_date.data

        # Get day, month and year from start date
        year_start_date, month_start_date, day_start_date = str(absence_start_date).split("-")
        
        # Convert to integer
        day_start_date = int(day_start_date)
        month_start_date = int(month_start_date)
        year_start_date = int(year_start_date)

        # Get day, month and year from end date
        year_end_date, month_end_date, day_end_date = str(absence_end_date).split("-")
        
        # Convert to integer
        day_end_date = int(day_end_date)
        month_end_date = int(month_end_date)
        year_end_date = int(year_end_date)

        # Create datetime objects with start and end dates
        absence_start_date = datetime(year_start_date, month_start_date, day_start_date)
        absence_end_date = datetime(year_end_date, month_end_date, day_end_date)

        # Get today date with date module
        date_today = date.today()

        # Convert today in to datetime object to compare dates
        today = datetime(date_today.year, date_today.month, date_today.day)

        # Create a day timedelta object period
        day = relativedelta(days=1)

        # Ensure absence start date is the allowed period of 15 days to register worker absence
        if absence_start_date > today or absence_start_date < today - day * 15:
            abort(400, description="Absence data out of 15 days allowed period to register absences!")

        # ensure absence end date is not lower than start date
        if absence_end_date < absence_start_date:
            abort(400, description="End date cannot be higher than start date!")

        # Query worker abscences
        worker_abscences = db_helper.query_worker_absences(worker_id)

        # Ensure user dont have an absence in same period of absence start date to register
        for abscence in worker_abscences:
            # Split start year, month and day
            start_year, start_month, start_day = abscence["start_date"].split("-")

            # Split end year, month and day
            end_year, end_month, end_day = abscence["end_date"].split("-")

            # Create datetime object to abscene start and end date
            registered_abscence_start_date = datetime(int(start_year), int(start_month), int(start_day))
            registered_abscence_end_date = datetime(int(end_year), int(end_month), int(end_day))

            if absence_start_date >= registered_abscence_start_date and absence_start_date <= registered_abscence_end_date:
                abort(400, description="Worker already have an abscence registered in the period you want to register!")

        # Find how many days workers works by week
        worlkload_days_by_week = worker_info[0]["workload_week"] / worker_info[0]["workload_week"]

        if worlkload_days_by_week > 7:
            worlkload_days_by_week = 7

        # Workload days by month
        workload_days_by_month = worlkload_days_by_week * 4

        # Get day payment
        day_payment = worker_info[0]["base_salary"] / workload_days_by_month

        # Get absence number of days
        absence_number_of_days = 0

        # Copy absence_start_date in to other variable
        itherate_absence_start_date = absence_start_date

        # Get number of days with absence
        while itherate_absence_start_date <= absence_end_date:
            # Increment one day
            itherate_absence_start_date += relativedelta(days=1)

            # Increment absence number of days
            absence_number_of_days += 1

        # Calculate absence total
        absence_total = absence_number_of_days * day_payment

        # Insert abscence
        db_helper.insert_absence(worker_id, absence_start_date.date(), absence_end_date.date(), absence_total)

        return jsonify({"success_response": f"Absence from <span class='personal-blue-color f-bold'>{absence_start_date.date()} - {absence_end_date.date()}</span> at worker <span class='personal-blue-color f-bold'>{worker_info[0]['fullname']}</span> registered with sucess!"})
    else:
        # Create HTML with errors
        errors = ""
        for _, error in form.errors.items():
            print(error)
            if isinstance(error[0], str):
                errors += f"<p>{error[0]}</p>"
            else:
                for _, v in error[0].items():
                    errors += f"<p>{v[0]}</p>"

        # Abort function and send errors as response
        abort(400, description=errors)

@app.route("/validate_and_register_benefit", methods=["POST"])
def validate_and_register_benefit():
    """ Validate and insert benefit in benefits table """

    # Benefit form data
    form_data = request.get_json()
    
    # Worker id
    worker_id = form_data["id"]

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Ensure worker id exists
    worker = db_helper.query_worker(worker_id)

    if not worker:
        abort(400, description="Worker not registered!")

    # Create Flask-WTF register benefit form
    form = registerBenefitForm(form_data=form_data)

    # Ensure form is valid
    if form.validate_on_submit():
        # Benefit
        worker_benefit = form.benefit.data

        # Actual date
        today = date.today()

        # Register benefit
        db_helper.insert_worker_benefit(today, float(worker_benefit), worker_id)

        # Return sucess message
        return jsonify({"success_response": f"Benefit of <span class='personal-blue-color f-bold'>{currency(worker_benefit)}</span> assigned with sucess at worker <span class='personal-blue-color f-bold'>{worker[0]['fullname']}</span>!"})
    else:
        # Create HTML with errors
        errors = ""
        for _, error in form.errors.items():
            print(error)
            if isinstance(error[0], str):
                errors += f"<p>{error[0]}</p>"
            else:
                for _, v in error[0].items():
                    errors += f"<p>{v[0]}</p>"

        # Abort function and send errors as response
        abort(400, description=errors)

@app.route("/remove_product_from_register_list", methods=["POST"])
def delete_product_from_register_list():
    """ Delete product selected by user and return sucess message """

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Get product description 
    description = request.data.decode('utf-8')

    # Query all user products in temp_register_list
    products_in_temp_register_list = db_helper.query_all_products_from_temp_register_list()

    # Ensure product is in the list
    has_product = False
    for product in products_in_temp_register_list:
        if description == product["description"]:
            has_product = True 

    if not has_product:
        abort(400, description="Product unlisted!")

    # Delete product from temp_register_list table
    db_helper.delete_product_from_temp_register_list(description)

    # Return sucess message
    return jsonify({"sucess_message": f"Product: {description} removed with sucess from list!"})


@app.route("/delete_all_products_from_order_list", methods=["POST"])
def delete_order_list():
    """ Delete products from temp_order_list table """

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Delete products from temp_order_list table
    db_helper.delete_all_products_from_order_list()

    return jsonify({"sucess_message": "All products deleted with sucess!"})

@app.route("/remove_all_products_from_register_list", methods=["POST"])
def delete_register_list():
    """ Delete register list and return sucess html """
    
    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Delete products from temp_register_list table
    db_helper.delete_all_products_from_temp_register_list()

    html = """
            <div class="mt-3">
                <h5 class="personal-blue-color">Your register list was deleted with sucess!</h5>
            </div>
            """

    # Return sucess html
    return jsonify({"delete_register_list_sucess_html": html})

@app.route("/delete_product", methods=["POST"])
def delete_product():
    """ Delete product from database """

    # Product id 
    product_id = request.data.decode('utf-8')

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Query product
    product = db_helper.query_product(product_id)

    print(product)
   
    # Ensure product is registered
    if not product:
        abort(400, description="Product not registered!")

    # Query services with product_id associated
    services_associated = db_helper.query_product_services_associated(product_id)

    print("services_associated")
    print(services_associated)

    service_update_information = []
    service_delete_information = []

    # Query product cost price
    product_financial = db_helper.query_product_financial(product_id)

    try:        
        # Start transaction
        db_helper.begin_transaction()

        # Delete product
        db_helper.delete_product(product_id)

        if services_associated:

            for service in services_associated:
                print(service)
                # Query service financial info
                service_info  = db_helper.query_service(service["id"])

                # Ensure service is registered
                if not service_info:
                    abort(400, description="Service not registered.")

                # Query service products associated info
                service_products = db_helper.query_service_products(service["id"])

                # Get service margin percentage
                service_margin_percentage = service_info[0]["margin_percentage"]

                print(type(service_margin_percentage))

                # Ensure service has more than 1 product associated else delete service
                if len(service_products) > 0:
                    new_service_cost_price = 0

                    # Calculate new service cost price
                    for p in service_products:
                        new_service_cost_price += product_financial[0]["cost_price"] * p["stock"]
                    
                    # New service sell price
                    new_service_sell_price = new_service_cost_price + (new_service_cost_price * (service_margin_percentage / 100))

                    # Append update prices information to service_update_information list
                    service_update_information.append({"service_description": service["description"],
                                                        "service_bar_code": service["bar_code"],
                                                        "old_service_cost_price": service["cost_price"],
                                                        "old_service_sell_price": service["sell_price"],
                                                        "new_service_cost_price": new_service_cost_price,
                                                        "new_service_sell_price": new_service_sell_price,
                                                        "margin_percentage": service_margin_percentage})
                
                    # Update service financial
                    db_helper.update_service_financial(service["id"], new_service_cost_price, new_service_sell_price, service_margin_percentage)
                else:
                    # Delete service
                    db_helper.delete_service(service["id"])

                    # Append delete informaation
                    service_delete_information.append({"service_description": service["description"], "service_bar_code": service["bar_code"]})
        
        # Commit transaction
        db_helper.commit()

    except (KeyError, AttributeError, IndexError, ValueError, RuntimeError, TypeError):
        # Rollback transaction
        db_helper.rollback()
        
        abort(400, description="Something wen't wtrong!")

    # Render delete_product_sucess.html
    delete_product_sucess_html = render_template("products_and_services_templates/delete_product_sucess.html", product_description=product[0]["description"], service_update_information=service_update_information, service_delete_information=service_delete_information)

    # Return rendered delete_product_sucess.html
    return jsonify({"delete_product_sucess_html": delete_product_sucess_html})

@app.route("/delete_service", methods=["POST"])
def delete_service():
    """ Delete service """

    # Service internal code
    service_id = request.data.decode("utf-8")

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Query service id
    service = db_helper.query_service(service_id)

    # Ensure service is registered
    if not service:
        abort(400, description="Service not registered!")

    # Delete service
    db_helper.delete_service(service_id)

    # Return sucess_message
    return jsonify({"delete_service_sucess_html": f"<div class='row mt-3 mb-3'><div class='col-lg-12 mt-3 mb-3'><h5 class='personal-blue-color text-center'>{service[0]['description']} deleted with sucess!</h5></div>"})

@app.route("/delete_product_from_order_list", methods=["POST"])
def delete_product_from_order_list():
    """ Delete product from order list """
    
    product_id = request.data.decode('utf-8')

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Delete product from order list
    db_helper.delete_product_from_temp_order_list(product_id)

    return jsonify({"sucess_message": "Product deleted from order with sucess!"})

@app.route("/delete_expense", methods=["POST"])
def delete_expense():
    """ Delete expense """

    # Expense id
    expense_id = request.data.decode("utf-8")

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Delete expense from expenses table
    db_helper.delete_expense(expense_id)

    return jsonify({"sucess_message": "Expense deleted with sucess!"})

@app.route("/delete_worker", methods=["POST"])
def delete_worker():
    """ Delete worker from workers table """

    # Worker number
    worker_id = request.data.decode("utf-8")

    # Inititate Database_helper object
    db_helper = current_user.db_connection

    # Ensure worker exists
    worker = db_helper.query_worker(worker_id)

    if not worker:
        abort(400, description="Worker not registered!")

    # Delete worker
    db_helper.delete_worker(worker_id)

    return jsonify({"sucess_message": "Worker deleted with sucess!"})

@app.route("/delete_absence", methods=["POST"])
def delete_absence():
    """ Delete absence from absences table """

    # Absence data to delete
    worker_id = request.get_json()["worker_id"]
    absence_start_date = request.get_json()["start_date"]

    print(absence_start_date)

    # Escape special characters
    worker_id = escape(worker_id)
    absence_start_date = escape(absence_start_date)

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Query worker
    worker = db_helper.query_worker(worker_id)

    # Ensure worker is registered
    if not worker:
        abort(400, description="Worker not registered!")
    
    # Delete absence
    db_helper.delete_absences(worker_id, start_date=absence_start_date)

    return jsonify({"success_response":"Absence deleted with sucess!"})

@app.route("/delete_benefit", methods=["POST"])
def delete_benefit():
    """ Delete benefit from benefits table """

    # Worker id
    worker_id = request.get_json()["worker_id"]

    # Benefit id
    benefit_id = request.get_json()["benefit_id"]
   
    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Query worker
    worker = db_helper.query_worker(worker_id)

    # Ensure worker is registered
    if not worker:
        abort(400, description="Worker not registered!")

    # Delete benefit
    db_helper.delete_worker_benefits(benefit_id)

    return jsonify({"sucess_message":"Benefit deleted with sucess!"})

@app.route("/delete_inventory", methods=["POST"])
def delete_inventory():
    """ Delete inventory from inventories table and delete inventory from inventories_products table"""

    # Inventory_id
    inventory_id = request.data.decode("utf-8")

    # Inititate Database_helper object
    db_helper = current_user.db_connection

    # Ensure inventory is registered
    try:
        inventory = db_helper.query_inventory(inventory_id)
    except IndexError:
        abort(400, description="Inventory doesn't exist!")

    # Inventory number
    inventory_number = inventory[0]["inventory_number"]

    # Delete inventory
    db_helper.delete_inventory(inventory_id)

    sucess_html = f"<h8 class='color-black'>Inventory with number <span class='personal-blue-color f-bold'>{inventory_number}</span> deleted with sucess!</h8>"

    return jsonify({"sucess_html": sucess_html})
 
@app.route("/update_worker_data", methods=["POST"])
def update_worker_data():
    """ Update worker data """

    # Worker data
    worker_data = request.get_json()
    worker_id = worker_data["id"]
    worker_fullname = worker_data["fullname"]
    worker_adress = worker_data["adress"]
    worker_contact = worker_data["contact"]
    worker_born_date = worker_data["born_date"]
    worker_section = worker_data["section"]
    worker_role = worker_data["role"]
    worker_workload_day = worker_data["workload_day"]
    worker_workload_week = worker_data["workload_week"]
    worker_base_salary = worker_data["base_salary"]

    # Convert data to match with database
    worker_data["worker_id"] = int(worker_data["id"])
    worker_data["workload_day"] = int(worker_data["workload_day"])
    worker_data["workload_week"] = int(worker_data["workload_week"])
    worker_data["base_salary"] = float(worker_data["base_salary"])

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Update worker data
    db_helper.update_worker_data(worker_id, worker_fullname, worker_adress, worker_contact, worker_born_date, worker_section, worker_role, worker_workload_day, worker_workload_week, worker_base_salary)

    return jsonify({"sucess_message": "Worker updated with sucess!"})

@app.route("/search_autocomplete")
def search_products_or_services_to_autocomplete():
    """ Search for products information and return a list rendered """

    # Arg to search
    q = request.args.get("q")

    print(q)

    # Split query and search type
    query, search_type = q.split("?")

    # Escape special characters
    query = escape(query)
    search_type = escape(search_type)

    # Initiate Database_helper object
    db_helper = current_user.db_connection

    # Filters
    filters = {"description_bar_code_filter": query,
                "category_filter": '',
                "sub_category_filters": [],
                "order_by_filter": "description",
                "asc_desc_filter": "asc"}

    if query == "" or query.isspace():
        # Return empty results
        search_results = []

        return jsonify({"search_results": search_results})
    
    # Ensure which search type to searcg
    if search_type == "product" or search_type == "order_product":
        # Search products with filters limited to 10 results
        search_results = db_helper.query_search_my_products_with_filters(filters, limit=5)
    elif search_type == "pos_registry_product_or_service":
        # Search products with filters limited to 10 results
        product_search_results = db_helper.query_search_my_products_with_filters(filters, limit=5)

        # Search services with filters
        service_search_results = db_helper.query_search_my_services_with_filters(filters)

        # Join two searchs
        search_results = product_search_results + service_search_results

    else:
        # Search services with filters
        search_results = db_helper.query_search_my_services_with_filters(filters)
    
    return jsonify({"search_results": search_results})

if __name__ == "__main__":
    app.run(debug=True)
