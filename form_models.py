from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, EmailField, DateField
from wtforms import DecimalField, RadioField, SelectField, SubmitField, ValidationError, FieldList, FormField
from wtforms.validators import DataRequired, Email, Length, InputRequired, EqualTo, NumberRange

def no_whitespace_check(form, field):
    if field.data == "" or field.data.isspace():
        raise ValidationError("Please complete the field.")
    
def validate_password_schema(form, field):
    from helpers import validate_password
    
    if not validate_password(field.data):
        raise ValidationError("Password must have at least one special character, one number, one lowercase, one uppercase letter and no white spaces.")
    
def validate_positive_values(form, field):
    if field.data <= 0:
        raise ValidationError("Prices must be higher than 0.")
    
def validate_required_stock_field(form, field):
    if field.data is None or field.data == "":
        raise ValidationError(message="Complete stock field.")
       
class loginUserForm(FlaskForm):
    email = EmailField('Email', [DataRequired(), Email(message="Please insert a valid email!"), Length(max=100), no_whitespace_check])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Login')
    remember = BooleanField()

class registerUserForm(FlaskForm):
    email = EmailField('Email', [DataRequired(), Email(message="Please insert a valid email!"), Length(max=100)])
    password = PasswordField('Password', [DataRequired(), Length(min=8, max=24, message="Password must have between 8 and 24!"), validate_password_schema])
    confirm_password = PasswordField('Confirm Password', [DataRequired(),  EqualTo('password', message="Passwords don't match!"), no_whitespace_check])    
    company_name = StringField('Company name', [DataRequired(), Length(min=3, max=30, message="Company name must have between 3 and 30 characters!")])
    currency = SelectField('Currency', [DataRequired(), no_whitespace_check], choices=["Dollars", "Euros"])
    submit = SubmitField('Register')

class personalCodeForm(FlaskForm):
    personal_code = PasswordField('Personal code',[DataRequired(), Length(min=8, max=8)])
    confirm_personal_code = PasswordField('Confirm personal code', [DataRequired(), EqualTo('personal_code', message="Personal codes don't match!"), Length(min=8, max=8)])
    submit = SubmitField('Set personal code')

class recoverPasswordForm(FlaskForm):
    email = EmailField('Email', [DataRequired(), Email(message="Please insert a valid email!"), Length(max=100)])
    personal_code = PasswordField('Personal code',[DataRequired(), Length(min=8, max=8)])
    submit = SubmitField('Recover password')

class defineNewPasswordForm(FlaskForm):
    new_password = PasswordField('New password', [DataRequired(), Length(min=8, max=24, message="Password must have between 8 and 24!"), validate_password_schema])
    confirm_new_password = PasswordField('Confirm new password', [DataRequired(),  EqualTo('new_password', message="Passwords don't match!")])
    submit = SubmitField('Define new password')

class defineNewPersonalCodeForm(FlaskForm):
    new_personal_code = PasswordField('New personal code',[DataRequired(), Length(min=8, max=8)])
    confirm_new_personal_code = PasswordField('Confirm new personal code', [DataRequired(), EqualTo('personal_code', message="Personal codes don't match!"), Length(min=8, max=8)])
    submit = SubmitField('Set personal code')

class changeCompanyNameForm(FlaskForm):
    company_name = company_name = StringField('Company name', [DataRequired(), Length(min=3, max=30, message="Company name must have between 3 and 30 characters!")])
    submit = SubmitField('Change company name')

class changeCurrencyForm(FlaskForm):
    currency = SelectField('Currency', [DataRequired(), no_whitespace_check], choices=["Dollars", "Euros"])
    submit = SubmitField('Change currency')

class changeEmailForm(FlaskForm):
    email = EmailField('New email', [DataRequired(), Email(message="Please insert a valid email!"), Length(max=100)])
    submit = SubmitField('Change email')

class authenticatePersonalCodeForm(FlaskForm):
    personal_code = PasswordField('Personal code',[DataRequired(), Length(min=8, max=8)])
    submit = SubmitField('Confirm')

class authenticatePasswordForm(FlaskForm):
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Confirm')

class registerProductForm(FlaskForm):
    product_description = StringField('Description', [DataRequired(message="Complete description field."), Length(min=5, max=30, message="Description must be between 5 and 30 characters long."), no_whitespace_check])
    bar_code = StringField('Bar code', [DataRequired(message="Complete bar code field."), Length(min=5, max=30, message="Bar code must be between 5 and 30 characters long."), no_whitespace_check])
    unity_m = SelectField('Unity of measurement', [DataRequired(message="Complete unity of measurement field.")], choices=["UN", "KG"])
    categories = SelectField('Category', [DataRequired(message="Complete categories field.")])
    sub_categories = SelectField('Sub category', [DataRequired(message="Complete sub categories field.")], choices=[])
    stock = DecimalField('Stock', [InputRequired(message="Complete stock field."), NumberRange(min=0, message="Stock must be 0 or more.")], default=0)
    cost_price = DecimalField('Cost price', [DataRequired(message="Complete cost price field."), validate_positive_values])
    sell_price = DecimalField('Sell price', [DataRequired(message="Complete sell price field."), validate_positive_values])
    submit_product = SubmitField('Send to confirm list')

class serviceProductsFields(FlaskForm):
    product = SelectField('Select product', [DataRequired(message="Complete product ")], choices=[])
    stock_associated =  DecimalField('Stock to deduct', [DataRequired(message="Complete stock field."), validate_positive_values], render_kw={"class": "service_stock"})

class registerServiceForm(FlaskForm):
    service_description = StringField('Description', [DataRequired(message="Complete description field"), Length(min=5, max=30, message="Description must be between 5 and 30 characters long."), no_whitespace_check])
    products_associated = FieldList(FormField(serviceProductsFields), min_entries=1)
    cost_price = DecimalField('Cost price', [DataRequired(message="Complete cost price field."), validate_positive_values])
    sell_price = DecimalField('Sell price', [DataRequired(message="Complete sell price field."), validate_positive_values]) 
    submit_service = SubmitField('Register service')

class searchAndEditForm(FlaskForm):
    search_field = StringField('Search and edit', [Length(max=30)])
    submit_search_and_edit = SubmitField('Search')

class checkBoxInputs(FlaskForm):
    check_box = BooleanField()

class searchProductsAndServicesForm(FlaskForm):
    description_bar_code_filter = StringField('Description or bar code:', [Length(max=30)])
    type_filter = SelectField('Type:', [DataRequired(message="Select product or service.")], choices=[("product", "Product"), ("service", "Service")])
    category_filter = SelectField('Category', [DataRequired(message="Please select a category.")])
    sub_category_filter = FieldList(FormField(checkBoxInputs), min_entries=1)
    order_by_filter = SelectField('Order by:', [DataRequired(message="Please select results order.")], choices=[("bar_code", "Bar code"), ("description", "Description"), ("cost_price", "Cost price"), ("sell_price", "Sell price"), ("margin_percentage", "Margin percentage")])
    asc_desc_filter = RadioField(choices=[("asc", "asc"), ("desc", "desc")])
    submit_search_all = SubmitField('Search')

class registerProductInOrderForm(FlaskForm):
    description = StringField('Description', [DataRequired(message="Complete description field."), Length(min=5, max=30), no_whitespace_check])
    bar_code = StringField('Bar code', [DataRequired(message="Complete bar code field."), Length(min=5, max=30), no_whitespace_check], render_kw={"readonly": "true"})
    cost_price = DecimalField('Cost price', [DataRequired(message="Complete cost price field."), validate_positive_values])
    sell_price = DecimalField('Sell price', [DataRequired(message="Complete sell price field."), validate_positive_values])
    quantity = DecimalField('Quantity', [DataRequired(message="Insert positive quantity.")]) 
    submit = SubmitField('Submit')

class chooseProductStocksForm():
    description = StringField('Description')
    submit = SubmitField('Submit')

class registerWasteForm(FlaskForm):
    stock = DecimalField('Stock to waste', [DataRequired(message="Insert positive stock to waste.")])
    waste_motives = SelectField('Waste motives', [DataRequired(message="Select a valid waste motive.")], choices=[(201, "Expired"), (202, "Damaged"), (203, "Transport Failure")])
    submit_waste = SubmitField('Register waste') 

class registerRegularizationForm(FlaskForm):
    stock = DecimalField('Stock to regularize', [InputRequired(message="Insert valid stock to regularize.")])
    submit_regularization = SubmitField('Register regularization')

class registerExpenseForm(FlaskForm):
    expenses = SelectField('Expense', [DataRequired(message="Select expense.")])
    total = DecimalField('Total', [DataRequired(message="Complete total field.")])
    month_year_dates = SelectField('Month/Year', [DataRequired(message="Select valid date.")])
    submit_expense = SubmitField('Register expense')

class checkExpensesForm(FlaskForm):
    year = SelectField('Year', [DataRequired(message="Please select year.")])
    month = SelectField('Month', [DataRequired(message="Please select month.")])
    check_expense = SubmitField('Check expense')

class registerWorkerForm(FlaskForm):
    fullname  = StringField('Fullname', [DataRequired(message="Complete fullname field."), Length(min=10, max=50)])
    born_date = DateField('Born date', [DataRequired(message="Complete born date field")])
    adress = StringField('Adress', [DataRequired(message="Complete adress field."), Length(min=10, max=50)])
    contact = StringField('Contact', [DataRequired(message="Complete contact field.")])
    section = SelectField('Section', [DataRequired(message="Select valid section.")])
    role = SelectField('Role', [DataRequired(message="Select valid role.")])
    workload_day = SelectField('Workload/day(Hours)', [DataRequired("Select valid hours workload for day.")])
    workload_week = SelectField('Workload/week(Hours)', [DataRequired("Select valid hours workload for week.")])
    base_salary = DecimalField('Base salary/month', [DataRequired(message="Complete base salary field.")])
    register_worker = SubmitField('Register') 

class registerAbsenceForm(FlaskForm):
    start_date = DateField('Start date', [DataRequired(message="Complete start date.")])
    end_date = DateField('End date', [DataRequired(message="Complete end date.")])
    register_absence = SubmitField('Register absence')

class consultAbsencesForm(FlaskForm):
    consult_dates = SelectField('Select date', [DataRequired(message="Select valid date.")])
    consult_absences = SubmitField('Consult absences')

class registerBenefitForm(FlaskForm):
    benefit = DecimalField('Benefit', [DataRequired(message="Complete benefit field.")])
    register_benefit = SubmitField('Register benefit')

class consultBenefitsForm(FlaskForm):
    consult_dates = SelectField('Select date', [DataRequired(message="Select a valid date.")])
    consult_benefits = SubmitField('Consult benefits')

class createInventoryForm(FlaskForm):
    category = SelectField('Category', [DataRequired(message="Select a valid category.")])
    sub_category_filter = FieldList(FormField(checkBoxInputs), min_entries=1)
    create_inventory = SubmitField('Create')

class selectProductsToInventoryForm(FlaskForm):
    selected_products = FieldList(FormField(checkBoxInputs), min_entries=1)
    submit = SubmitField('Create inventory')
