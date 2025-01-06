from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Admin model
class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

# Provider model
class Provider(db.Model):
    __tablename__ = 'providers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    contact = db.Column(db.String(10), nullable=True)
    experience = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String, nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String, nullable=False)
    filename = db.Column(db.String, nullable=False)
    file_path = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, default=0.0)
    active = db.Column(db.Boolean, default=False)
    balance = db.Column(db.Float, default=0.0)

    subtype_id = db.Column(db.Integer, db.ForeignKey('service_subtypes.id'))
    subtype = db.relationship('ServiceSubtype', back_populates='providers')

    # Relationship to service requests
    service_requests = db.relationship('ServiceRequest', backref='provider', lazy=True)

# Service Subtype model
class ServiceSubtype(db.Model):
    __tablename__ = 'service_subtypes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('service_categories.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)

    # Relationship to providers
    providers = db.relationship('Provider', back_populates='subtype')

# Customer model
class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    contact = db.Column(db.String(10), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, default=True)

    # Relationships to service requests and reviews
    service_requests = db.relationship('ServiceRequest', backref='customer', lazy=True)
    reviews = db.relationship('Review', backref='customer', lazy=True)

# Service Category model
class ServiceCategory(db.Model):
    __tablename__ = 'service_categories'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    
    # Relationship to service subtypes
    subtypes = db.relationship('ServiceSubtype', backref='category', lazy=True)

# ServiceRequest model
class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    subtype_id = db.Column(db.Integer, db.ForeignKey('service_subtypes.id'), nullable=False)
    date_of_request = db.Column(db.DateTime, default=datetime.utcnow)
    date_of_completion = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.Enum('requested', 'assigned', 'rejected', 'completed', 'closed', 'flagged', name="status_enum"), default='requested')
    remarks = db.Column(db.Text, nullable=True)
    active = db.Column(db.Boolean, default=True)

    # Relationships to subtype and review
    subtype = db.relationship('ServiceSubtype', backref='service_requests')
    reviews = db.relationship('Review', backref='service_request', lazy=True)

# Review model
class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_requests.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    comment = db.Column(db.Text, nullable=True)
