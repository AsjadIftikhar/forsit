## Setup Instructions

### Dependencies
1. Python 3
2. PostgreSQL


Follow these steps to set up and run the Forsit application on your local machine.

1. Change to the Forsit code directory:

    ```bash
    cd <forsit/code>
    ```

2. Create a virtual environment (venv):

    ```bash
    python3 -m venv venv
    ```

3. Activate the virtual environment:

    ```bash
    source venv/bin/activate
    ```

4. Install the required packages from the `requirements.txt` file:

    ```bash
    pip install -r requirements.txt
    ```

5. Create a `.env` file in your project directory and paste the following link, replacing `<username>`, `<password>`, and `<db_name>` with your database credentials:

    ```
    DATABASE_URL=postgresql://<username>:<password>@localhost/<db_name>
    ```

6. Run database migrations using Alembic:

    ```bash
    alembic upgrade head
    ```

7. Open a Python console:

    ```bash
    python
    ```

8. In the Python console, import and run the database seed script:

    ```python
    import app.database.seed
    ```

9. Open your web browser and go to the following address:

    ```
    http://127.0.0.1:8000/docs
    ```

You should now have the Forsit application up and running locally, and you can access the API documentation via your web browser.

### API Endpoints

The Forsit API provides the following endpoints:

- **Read Products**: Get a list of products with optional pagination.
- **Create Product**: Create a new product.
- **Update Product**: Update an existing product.
- **Delete Product**: Delete a product by ID.
- **Update Stock**: Update the stock quantity of a product.
- **Get Sales by Filters**: Get a list of sales based on various filters such as product, category, and date range.
- **Create Sale**: Create a new sale for a product.
- **Analyze Sales Revenue by Interval**: Analyze the total revenue within a specified time interval.
- **Compare Revenue by Date Range**: Compare total revenue between two date ranges.
- **Compare Revenue by Categories**: Compare total revenue between two product categories.

These endpoints allow you to interact with the Forsit application and manage products and sales efficiently. For more details visit http://127.0.0.1:8000/docs for complete documentation.

## Database Schema

The Forsit application uses a PostgreSQL database with the following schema:

### Categories

- **Table Name**: `categories`
- **Description**: This table stores product categories.
- **Columns**:
  - `id`: Unique identifier for the category.
  - `name`: The name of the category.
- **Relationships**:
  - One-to-Many relationship with the `products` table, representing that a category can have multiple products.

### Products

- **Table Name**: `products`
- **Description**: This table stores information about individual products.
- **Columns**:
  - `id`: Unique identifier for the product.
  - `name`: The name of the product.
  - `description`: A description of the product.
  - `price`: The price of the product.
  - `margin`: The margin percentage for the product.
  - `stock`: The quantity of the product in stock.
  - `is_deleted`: A flag indicating whether the product has been marked as deleted.
  - `category_id`: Foreign key referencing the `categories` table, indicating the category to which the product belongs.
- **Relationships**:
  - Many-to-One relationship with the `categories` table, representing that a product belongs to a category.
  - One-to-Many relationships with the `sales` and `inventory_tracking` tables, indicating that a product can have multiple sales and inventory tracking records.

### Sales

- **Table Name**: `sales`
- **Description**: This table stores information about product sales.
- **Columns**:
  - `id`: Unique identifier for the sale.
  - `sale_date`: The date when the sale occurred.
  - `quantity`: The quantity of the product sold.
  - `total`: The total sale amount.
  - `revenue`: The revenue generated from the sale.
  - `product_id`: Foreign key referencing the `products` table, indicating the product associated with the sale.
- **Relationships**:
  - Many-to-One relationship with the `products` table, representing the product associated with the sale.

### Inventory Tracking

- **Table Name**: `inventory_tracking`
- **Description**: This table tracks changes in product inventory.
- **Columns**:
  - `id`: Unique identifier for the inventory tracking entry.
  - `quantity`: The quantity of the product in inventory.
  - `timestamp`: The timestamp when the inventory tracking entry was recorded.
  - `product_id`: Foreign key referencing the `products` table, indicating the product associated with the inventory tracking entry.
- **Relationships**:
  - Many-to-One relationship with the `products` table, representing the product associated with the inventory tracking entry.

These tables and their relationships form the database schema for the Forsit application, allowing efficient management of products, sales, and inventory tracking.

## Project Configuration

The Forsit project relies on the following essential libraries for project configuration:

### Alembic

- **Purpose**: Alembic is used for database migrations. It helps manage changes to the database schema over time, ensuring that the database structure remains in sync with the application's evolving data model.

### Faker

- **Purpose**: Faker is a Python library used for generating random and fake data. It plays a crucial role in seeding the database with test data, making it easier to develop and test

## Essential Libraries for Later

When improving this Forsit project, it's crucial to consider libraries that maybe necessary for project configuration, especially those related to authentication and email services.

### Authentication

- **Library**: [FastAPI OAuth](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- **Purpose**: Authentication is a fundamental aspect of any web application. FastAPI OAuth is used to implement OAuth2-based authentication, providing secure and standardized methods for user identity verification. This library ensures that only authorized users can access protected resources, enhancing the overall security of the application.

### Email Service

- **Library**: [SMTP Integration](https://docs.python.org/3/library/smtplib.html)
- **Purpose**: Email communication is essential for various aspects of the application, such as user notifications, password reset requests, and more. By integrating SMTP (Simple Mail Transfer Protocol), the application can send emails to users when necessary. This library enables reliable email communication, enhancing user experience and system functionality.

These libraries are essential for project configuration, with FastAPI OAuth ensuring secure user authentication and SMTP integration enabling seamless email communication. Including these libraries from the outset is crucial to the overall functionality and security of the Forsit project.

## Handling Datetime Across Timezones

When dealing with datetime data in Python and a database like PostgreSQL, it's important to consider the differences in timezones between your application, the database, and the end-users. Here are some essential practices to handle datetime effectively:

### 1. Timezone-Aware Datetime Objects

Always use timezone-aware datetime objects to store and manipulate datetime data. In Python, you can achieve this using the `datetime` module along with the `pytz` library:

```python
from datetime import datetime
import pytz

# Create a timezone-aware datetime object
aware_datetime = datetime(2023, 1, 15, 12, 0, tzinfo=pytz.UTC)
