# 📦 SmallBiz
#### 🎥 Video Demo: https://youtu.be/_iNC1dtRF7I  
#### 📝 Description  
**SmallBiz** is a web application designed to support small retail businesses by providing an organized, fast, and efficient system for managing products, inventories, sales, and finances.  
The project was inspired by real ERP systems such as **SAP**, aiming to recreate some of their essential features in a simplified, accessible way — based on my previous professional experience working in retail, logistics, and warehouse operations.

---

## 🧭 Introduction

The idea for this project came from noticing that many small businesses in my community rely on outdated or manual tools for managing finances and logistics.  
Having worked for over a decade in store and warehouse environments, I had firsthand experience with inventory control, product handling, and operational workflows — which directly influenced the design of SmallBiz.

SmallBiz helps business owners by offering:

- Product registration and management  
- Inventory tracking  
- Waste and sales logging  
- Cash flow and monthly financial reports  
- Visual analytics using **Chart.js**  
- A cash register system with two modes:  
  - **Manual mode** – enter barcodes manually  
  - **Barcode reader mode** – use a real barcode scanner for faster input  

---

## 🎨 Design

SmallBiz was built to be simple, intuitive, and user-friendly.

- **Backend:** Python + Flask  
- **Frontend:** HTML, CSS, Bootstrap  
- **Dynamic behavior:** JavaScript + AJAX (without reloading pages)

The project relies on 8 core files that ensure maintainability, security, scalability, and code organization:

- `styles.css`  
- `script.js`  
- `app.py`  
- `db_helper.py`  
- `form_models.py`  
- `helpers.py`  
- `smallbiz_project.db`  
- `pos_sales.db`

### 📁 Core Files Overview

- **app.py**  
  Initializes and configures the Flask app, manages database connections, and handles route security.

- **helpers.py**  
  Provides data-cleaning functions, financial calculations, and a custom `login_required` decorator.

- **db_helper.py**  
  Connects the app to `smallbiz_project.db` and organizes database operations for each user.

- **form_models.py**  
  Provides secure form handling using **Flask-WTF** with CSRF protection.

- **styles.css**  
  Defines responsive behavior and custom styling.

- **script.js**  
  Handles AJAX requests, updates UI dynamically, and manages client-side interactions.

- **smallbiz_project.db**  
  Main database storing users, companies, sales, wastes, employees, and other business data.

- **pos_sales.db**  
  Stores all records related to POS (cash register) operations.

---

## 🔐 Security

SmallBiz includes several security measures:

- **Content-Security-Policy (CSP)** to block unauthorized scripts  
- **Flask-WTF + CSRF tokens** to protect forms  
- **Two-Factor Authentication** for sensitive operations  
- **Parameterized SQL queries** to prevent SQL injection  
- **Encrypted passwords and personal codes**  
- **Flask-Login** for secure session management  

---

# ⚙️ Prerequisites

- Python **3.12+**  
- pip  
- git (optional)

---

# 🚀 Installation & Run Guide

```bash
# Verify installed tools
python3 --version
pip --version
git --version 

# Create and activate virtual environment (Linux/MacOS)
python3 -m venv venv
source venv/bin/activate

# Create and activate virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
flask run
```
---

## ✅ Conclusion

**SmallBiz** was my final project for the online course **CS50x – Introduction to Computer Science** from Harvard University.  
This project allowed me to deepen and reinforce the concepts and skills I learned throughout the course by applying them in a practical, real-world web application.
# Deactivate when finished
deactivate
