# 🍽️ Canteen - Django Canteen Management System

A modern, secure, and user-friendly canteen management system built with Django. This application allows users to browse menu items, place orders, and manage their profiles, while staff can manage orders, add/edit menu items, and track order status.

## ✨ Features

### 👤 User Features
- **User Registration & Authentication**: Secure login/register system with profile management
- **Menu Browsing**: View available food items with categories and prices
- **Shopping Cart**: Add/remove items, adjust quantities, and manage cart
- **Order Management**: Place orders, track order status, and view order history
- **Profile Management**: Update personal information including department, cabin, block, and floor details
- **Payment Options**: Support for Cash on Delivery (COD) and online payment integration

### 👨‍💼 Staff/Admin Features
- **Dashboard**: Comprehensive overview of all orders with status tracking
- **Menu Management**: Add, edit, and delete food items with image uploads
- **Order Processing**: Update order status (pending → accepted → completed)
- **Category Management**: Organize menu items by categories
- **Order Analytics**: View order history and manage customer orders

### 🔒 Security Features
- **CSRF Protection**: Built-in protection against cross-site request forgery
- **Authentication Required**: Secure access control for user-specific features
- **Staff Permissions**: Role-based access control for admin functions
- **Input Validation**: Comprehensive form validation and data sanitization
- **Environment Variables**: Secure configuration management

## 🛠️ Technology Stack

- **Backend**: Django 5.1.7
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Image Handling**: Pillow
- **Configuration**: python-decouple
- **Authentication**: Django's built-in authentication system

## 📋 Prerequisites

Before running this application, make sure you have the following installed:

- Python 3.8 or higher
- pip (Python package installer)
- Git


The application will be available at `http://127.0.0.1:8000/`

## 📁 Project Structure

```
canteenO2/
├── canteenO2/                 # Django project settings
│   ├── __init__.py
│   ├── settings.py           # Project configuration
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── home/                     # Main application
│   ├── __init__.py
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── forms.py             # Form definitions
│   ├── admin.py             # Admin interface configuration
│   ├── apps.py              # App configuration
│   └── templates/           # HTML templates
│       ├── base.html
│       ├── home.html
│       ├── login.html
│       ├── register.html
│       ├── cart.html
│       ├── orders.html
│       └── ...
├── public/static/           # Static files (images, CSS, JS)
├── staticfiles/            # Collected static files
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── env_example.txt        # Environment variables example
└── README.md             # This file
```

## 🗄️ Database Models

### Core Models

- **User**: Django's built-in User model with extended Profile
- **ItemCategory**: Food categories (e.g., Main Course, Beverages, Desserts)
- **Item**: Food items with name, price, image, and category
- **Cart**: Shopping cart with user, payment status, and order status
- **CartItem**: Individual items in cart with quantities
- **Profile**: Extended user profile with department and location details

## 🔐 User Roles & Permissions

### Regular Users
- Browse menu items
- Add items to cart
- Place orders
- View order history
- Manage profile

### Staff Members
- All user permissions
- Access admin dashboard
- Manage menu items
- Process orders
- Update order status

### Superusers
- All staff permissions
- Access Django admin interface
- Manage users and categories
- System configuration

## 🍽️ Menu Management

### Adding Menu Items
1. Login as staff member
2. Navigate to Dashboard
3. Click "Add Item"
4. Fill in item details:
   - Item name
   - Price
   - Category
   - Image upload
5. Save the item

### Managing Categories
Categories are managed through the Django admin interface:
1. Access `/admin/`
2. Navigate to "Item Categories"
3. Add, edit, or delete categories

## 📦 Order Process

### For Customers
1. **Browse Menu**: View available items on the home page
2. **Add to Cart**: Click "Add to Cart" on desired items
3. **Manage Cart**: Adjust quantities or remove items
4. **Confirm Order**: Review cart and proceed to checkout
5. **Payment**: Choose payment method (COD/Online)
6. **Track Order**: Monitor order status in "Orders" section

### For Staff
1. **View Orders**: Check dashboard for new orders
2. **Process Orders**: Update status from "Pending" to "Accepted"
3. **Complete Orders**: Mark orders as "Completed" when ready
4. **Manage Inventory**: Add/remove items based on availability

## 🔧 Configuration

### Development Settings
- `DEBUG=True`: Enable debug mode
- `ALLOWED_HOSTS`: Configure allowed hosts
- `SECRET_KEY`: Set a secure secret key

### Production Settings
- Set `DEBUG=False`
- Configure proper `ALLOWED_HOSTS`
- Use environment variables for sensitive data
- Set up proper database (PostgreSQL recommended)
- Configure static file serving

### Email Configuration
To enable email notifications, add email settings to `.env`:

```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

