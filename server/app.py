from flask import Flask, jsonify, request, abort
from flask_migrate import Migrate
from models import db, initialize_db, Vendor, Sweet, VendorSweet

# Initialize the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Database URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and migration
initialize_db(app)
migrate = Migrate(app, db)

# Routes
@app.route('/vendors', methods=['GET'])
def get_vendors():
    vendors = Vendor.query.all()
    result = [{'id': vendor.id, 'name': vendor.name} for vendor in vendors]
    return jsonify(result)

@app.route('/vendors/<int:id>', methods=['GET'])
def get_vendor(id):
    vendor = Vendor.query.get(id)
    if not vendor:
        abort(404, {'error': 'Vendor not found'})
    
    vendor_sweets = vendor.vendor_sweets
    vendor_sweets_result = [{
        'id': vs.id,
        'price': vs.price,
        'sweet': {'id': vs.sweet.id, 'name': vs.sweet.name},
        'sweet_id': vs.sweet_id,
        'vendor_id': vs.vendor_id
    } for vs in vendor_sweets]
    
    result = {
        'id': vendor.id,
        'name': vendor.name,
        'vendor_sweets': vendor_sweets_result
    }
    return jsonify(result)

@app.route('/sweets', methods=['GET'])
def get_sweets():
    sweets = Sweet.query.all()
    result = [{'id': sweet.id, 'name': sweet.name} for sweet in sweets]
    return jsonify(result)

@app.route('/sweets/<int:id>', methods=['GET'])
def get_sweet(id):
    sweet = Sweet.query.get(id)
    if not sweet:
        abort(404, {'error': 'Sweet not found'})
    
    result = {
        'id': sweet.id,
        'name': sweet.name
    }
    return jsonify(result)

@app.route('/vendor_sweets', methods=['POST'])
def create_vendor_sweet():
    data = request.get_json()
    price = data.get('price')
    vendor_id = data.get('vendor_id')
    sweet_id = data.get('sweet_id')
    
    # Validate the data
    if price is None or price < 0:
        abort(400, {'errors': ['Invalid price']})
    
    vendor = Vendor.query.get(vendor_id)
    sweet = Sweet.query.get(sweet_id)
    
    if not vendor or not sweet:
        abort(400, {'errors': ['Invalid vendor or sweet ID']})
    
    vendor_sweet = VendorSweet(price=price, vendor_id=vendor_id, sweet_id=sweet_id)
    db.session.add(vendor_sweet)
    db.session.commit()
    
    result = {
        'id': vendor_sweet.id,
        'price': vendor_sweet.price,
        'sweet': {'id': vendor_sweet.sweet.id, 'name': vendor_sweet.sweet.name},
        'sweet_id': vendor_sweet.sweet_id,
        'vendor': {'id': vendor_sweet.vendor.id, 'name': vendor_sweet.vendor.name},
        'vendor_id': vendor_sweet.vendor_id
    }
    return jsonify(result), 201

@app.route('/vendor_sweets/<int:id>', methods=['DELETE'])
def delete_vendor_sweet(id):
    vendor_sweet = VendorSweet.query.get(id)
    if not vendor_sweet:
        abort(404, {'error': 'VendorSweet not found'})
    
    db.session.delete(vendor_sweet)
    db.session.commit()
    
    return jsonify({}), 204

# Start the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
