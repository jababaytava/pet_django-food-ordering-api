Food Ordering API
A backend service for managing food orders in a restaurant. Supports user authentication, menu browsing, table assignment, order creation, and Telegram integration for order notifications and management.

Tech Stack
Python, Django, Django REST Framework (DRF)
JWT authentication (djangorestframework-simplejwt)
PostgreSQL (SQLite supported for testing)
Celery + RabbitMQ for background processing
Telegram Bot API for notifications and order status management
Docker + Docker Compose
Swagger UI for auto-generated documentation
Pytest + pytest-django for testing

Features
User registration and login with JWT
Menu management (only active dishes are available)
Admin interface for managing dishes and tables
Table assignment and multiple dish selection in a single order
Validation to prevent ordering inactive dishes
Telegram bot integration:
Sends order details to the restaurant chat
Inline buttons to accept/reject orders
Option to mark orders as completed
Complete test coverage for users, menu, orders, and tables

JWT Authentication
Supports:
access token – for authentication
refresh token – for renewing access tokens

Running with Docker
docker-compose up --build

Default URLs:
API: http://localhost:8000
Swagger Docs: http://localhost:8000/api/docs/

Running Tests
pytest

Telegram Bot Integration
Create a bot via BotFather and obtain the bot token.

Get your chat_id.

Add the following variables to your .env file:

env
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
TELEGRAM_SECRET=your_custom_secure_string
BACKEND_URL=http://web:8000

API Endpoints
Method	Endpoint	Description
POST	/api/users/register/	Register a new user
POST	/api/token/	Obtain JWT tokens
GET	/api/menu/dishes/	List available dishes
POST	/api/orders/create/	Create a new order
GET	/api/orders/	Retrieve user orders
POST	/api/orders/update-status/	Update order status (Telegram)



