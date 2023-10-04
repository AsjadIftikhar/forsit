import random
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import Category, Product, Sale, InventoryTracking
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Create a Faker instance for generating random data
fake = Faker()


# Load environment variables from .env file
load_dotenv()

# Retrieve the database URL from the environment
database_url = os.getenv("DATABASE_URL")

# Create a SQLAlchemy engine and session
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
session = Session()


# Function to generate random datetime within a range
def random_datetime(start_date, end_date):
    return start_date + timedelta(
        seconds=random.randint(0, int((end_date - start_date).total_seconds()))
    )


# Function to create random data for categories
def create_random_category():
    category = Category(name=fake.unique.word())
    return category


# Function to create random data for products
def create_random_product(category):
    product = Product(
        name=fake.unique.word(),
        description=fake.sentence(),
        price=random.uniform(1.0, 100.0),
        margin=random.uniform(0.1, 0.5),
        stock=random.randint(0, 100),
        category=category,
    )
    return product


# Function to create random data for sales
def create_random_sale(product):
    sale = Sale(
        sale_date=random_datetime(datetime(2022, 1, 1), datetime(2023, 1, 1)),
        quantity=random.randint(1, 10),
        total=random.uniform(10.0, 500.0),
        revenue=random.uniform(1.0, 100.0),
        product=product,
    )
    return sale


# Function to create random data for inventory tracking
def create_random_inventory_tracking(product):
    inventory_tracking = InventoryTracking(
        quantity=random.randint(0, 50),
        timestamp=random_datetime(datetime(2022, 1, 1), datetime(2023, 1, 1)),
        product=product,
    )
    return inventory_tracking


# Seed the database with random data
try:
    for _ in range(10):  # Create 10 categories
        category = create_random_category()
        session.add(category)
        for _ in range(10):  # Create 10 products per category
            product = create_random_product(category)
            session.add(product)
            for _ in range(5):  # Create 5 sales and inventory tracking entries per product
                sale = create_random_sale(product)
                session.add(sale)
                inventory_tracking = create_random_inventory_tracking(product)
                session.add(inventory_tracking)

    session.commit()
    print("Database seeded successfully.")
except Exception as e:
    session.rollback()
    print("Error seeding the database:", str(e))
finally:
    session.close()
