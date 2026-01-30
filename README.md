FurniStore — Django Furniture E-Commerce Website

FurniStore is a modern furniture e-commerce web application built with Django, featuring product listings, cart, wishlist, checkout, and order management with a stylish frontend.

Features
Core E-Commerce

Product listing with categories

Product detail pages

Shopping cart (session-based)

Wishlist 

Checkout & order placement

Order & OrderItem management

Order success confirmation page

User System

User authentication (Login / Logout)

Wishlist linked to user account

Orders linked to authenticated users

Admin Panel

Manage products & categories

View customer orders

Order items stored per order

Frontend

Modern responsive UI

Hero section & product cards

Dropdown category menu

Clean navbar & footer

Optimized image handling

Mobile-friendly layout

Tech Stack

Backend: Django (Python)

Frontend: HTML5, CSS3 (Custom, no framework)

Database: SQLite (default)

Authentication: Django Auth

Version Control: Git & GitHub

📂 Project Structure
furniture_store/
│
├── shop/               # Products, categories, wishlist, homepage
├── cart/               # Cart & checkout logic
├── templates/          # HTML templates
├── static/             # CSS & static assets
├── manage.py
└── requirements.txt

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/YOUR_USERNAME/furnistore-django.git
cd furnistore-django

git clone https://github.com/YOUR_USERNAME/furnistore-django.git
cd furnistore-django
2️⃣Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Migrations
python manage.py migrate

5️⃣ Create Superuser
python manage.py createsuperuser

6️⃣ Run Server
python manage.py runserver


Open browser:

http://127.0.0.1:8000/
