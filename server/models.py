from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# Define Vendor model
class Vendor(db.Model):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    # Relationship with VendorSweet
    vendor_sweets = relationship('VendorSweet', back_populates='vendor', cascade='all, delete')

    def __repr__(self):
        return f'<Vendor {self.name}>'

# Define Sweet model
class Sweet(db.Model):
    __tablename__ = 'sweets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    # Relationship with VendorSweet
    vendor_sweets = relationship('VendorSweet', back_populates='sweet', cascade='all, delete')

    def __repr__(self):
        return f'<Sweet {self.name}>'

# Define VendorSweet model
class VendorSweet(db.Model):
    __tablename__ = 'vendor_sweets'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)

    # Foreign keys to Vendor and Sweet
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    sweet_id = db.Column(db.Integer, db.ForeignKey('sweets.id'), nullable=False)

    # Relationships
    vendor = relationship('Vendor', back_populates='vendor_sweets')
    sweet = relationship('Sweet', back_populates='vendor_sweets')

    def __repr__(self):
        return f'<VendorSweet vendor={self.vendor.name}, sweet={self.sweet.name}, price={self.price}>'

# Initialize the database
def initialize_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
