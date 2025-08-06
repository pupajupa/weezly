# Weezly: Django web store

[![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=Maksim+Antikhovitch+)](https://git.io/typing-svg)
![Screenshot 2022-01-09 at 17-04-55 Django Online Shop](/weezly_shop/online_shop/static/images/store.png)

This project is a simple but usable online shop written with Django. The app provides a custom dashboard to manage products and orders. Users can like a product, add it to the cart, and proceed to checkout. Order processing is supported, but the payment is handled using a Paypal API system.

![Preview](/weezly_shop/online_shop/static/images/preview.png)

## 🚀 Features

### 👤 User Capabilities

-   Browse and search products by category
-   Add to cart, favorite items, place orders
-   View order history and profile
-   Email confirmation, password reset via SMTP
-   Pay for orders using PayPal

### 🛠️ Manager Dashboard

Accessible at [`/accounts/login/manager`](http://127.0.0.1:8000/accounts/login/manager)

-   Add/edit/delete products and categories
-   View and manage all orders
-   View user details and permissions
-   For demo:

        Email: manager@example.com

        Password: managerpass1234

### ⚙️ System Features

-   Background email and order task processing with **Celery** + **Redis**
-   Payment integration with **PayPal REST API**
-   Email delivery using **SMTP**
-   Role-based access control
-   Fully responsive UI with Bootstrap

---

## 🧱 Tech Stack

-   Python 3.x
-   Django 4.x
-   Celery + Redis (background tasks)
-   PayPal REST API (payments)
-   SMTP (mail service, e.g. Gmail or Mailtrap)
-   Bootstrap (frontend)
-   SQLite (default), or PostgreSQL for production

---

## ⚙️ Installation Guide

### 🔧 Backend Setup

1.  Clone the repository

        git clone https://github.com/pupajupa/weezly.git
        cd weezly/weezly_shop

2.  Create virtual environment

        python3 -m venv venv
        Linux/Mac: source venv/bin/activate
        Windows: venv\\Scripts\\activate

3.  Install dependencies

        pip install -r requirements.txt

4.  Apply migrations

        python manage.py migrate

5.  Create superuser

        python manage.py createsuperuser

6.  Start development server
    python manage.py runserver

### 🔁 Celery & Redis Setup

Make sure Redis is running (default: localhost:6379), then in another terminal:

        celery -A weezly_shop worker --loglevel=info

### 💌 SMTP Configuration (Example: Gmail)

In .env or settings file:

        EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
        EMAIL_HOST=smtp.gmail.com
        EMAIL_PORT=587
        EMAIL_USE_TLS=True
        EMAIL_HOST_USER=your_email@gmail.com
        EMAIL_HOST_PASSWORD=your_app_password

### 💳 PayPal Integration

Add to .env:

        PAYPAL_CLIENT_ID=your_paypal_client_id
        PAYPAL_CLIENT_SECRET=your_paypal_secret

### 🧪 Running Tests

      python manage.py test
