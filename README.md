# SmallBiz
#### Video Demo:  https://youtu.be/_iNC1dtRF7I
#### Description:
**Smallbiz** is a web application/tool designed to retail business.

## Introduction
The creation of this project came with the idea of helping small business in my commmunity. 
They use rudimentary financial and logistic systems, so I decided to create an web app to make this process easier, faster and efficient, so they can concentrate in other important details to improve their business.

The application is based on product registration and management through inventories and records of wastes/sales. User can consult his business cash flow and other important details through charts made with **Javascript** library *Chart.js* and financial mensal reports. **Smallbiz** also contains a cash register system with two modes - *Manual* and *Bar code reader*. The difference between this two modes, as we can see by their names. In first mode, users have to digit the product bar code mannually and in the second, if users have a **bar code reader** system, they can use it to read products bar code and make the product register way faster.
## Design
Smallbiz was designed to be user-friendly and simple.
I used **Python** and **Flask** in **Smallbiz** back-end and used **HTML** with **CSS** and **Bootstrapp** library in front-end. Used **Javascript** together with **Ajax** to make most of the requests and responses dinamically without page reload, to give to user an efficient and fast *web application*.

**Smallbiz** has 8 important files in app maintenance, security and scalabilty and code organization:

* styles.css
* script.js
* app.py
* db_helper.py
* form_models.py
* helpers.py
* smallbiz_project.db
* pos_sales.db

The file **app.py** starts and configures my Flask app and his security, manages the connections with databases and the user acess to app routes.

The file **helpers.py** contains functions to clean data sent from client-side, do financial calculations and has an addapted wrapped Flask decorator - *login_required* - function.

The file **db_helper.py** connects **app.py** with **smallbiz_project.db**. This module contains a class that initiates an object with user id, and helps and organize the connection to smallbiz_project database.

The file **form_models.py** contains forms using **WTF-Forms** from **Flask-WTF** to ensure ill-intentionated users dont try to manipulate forms and prevent *Cross-Site* attacks.

The file **styles.css** has some CSS and media queries to some *Html* elements responde in a responsive way depending on users device screen size.

The file **script.js** has an important role in the way app works. It's what makes the app dynamic through dinamic requests to server-side, receives the responses and send to client-side with help of **Ajax**. Also helps in the way users interact with forms and make some elements responsive to differente devices screen size.

The remaining files are the databases used by my web app. **smallbiz_project.db** is the main, this database save all users information and all their companies sales, wastes, workers, etc. **pos_sales.db** saves information relative to *Cash register system* purchases.
## Security
To ensure the app security I used some tools and configurations provided by Flask documentation:
* Configured **Content-Security-Police** to ensure only internal scripts are loaded, avoiding scripts by ill-intentionated users.
* Used **WTF-Forms** from **Flask-WTF** to ensure the forms security through a secret token passed to the form in client-side preventing *Cross-Site* and *XSS* attacks.
* Implemented **Two-Authenticator-Factors** where users must set a personal code set after first login, and everytime users want to change password, email or even personal code have to pass by this system.
* To prevent **SQL injection** all requests made by users that need a connection with databases, are passed with placeholders in queries.
* All passwords and personal codes in databases are **encrypted** to maintain users information secure.
* To manage users login and sessions security I used **Flask-Login**.













