from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object("config.Config")

db = SQLAlchemy(app)


# create of model 

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone
        }
        

#create table in database
with app.app_context():
    db.create_all()
    

#create routes

@app.route("/contacts", methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    return jsonify({'contacts': [contact.serialize() for contact in contacts]})

@app.route("/contacts", methods=['POST'])
def create_contact():
    data = request.get_json()
    name = data['name']
    email = data['email']
    phone = data['phone']
    
    new_contact = Contact(name=name, email=email, phone=phone)
    
    existing_contact = Contact.query.filter_by(email=email).first()
    
    if existing_contact:
        return jsonify({'message': 'Ya hay un contacto con este email'}), 409  # Conflict HTTP status code
    else:
        db.session.add(new_contact)
        db.session.commit()
        return jsonify(
            {
                'message': 'contacto creado con éxito', 
                'contact': new_contact.serialize()
            }
            ), 201


@app.route("/contacts/<int:id>", methods=['GET'])
def get_contact(id):
    contact = Contact.query.filter_by(id=id).first()
    
    if not contact:
        return jsonify({'message': 'contacto no encontrado'}), 404
    
    return jsonify({'contact': contact.serialize()}), 200

@app.route("/contacts/<int:id>", methods=['PATCH'])
def update_contact(id):
    contact = Contact.query.get_or_404(id)
    
    if contact:
        data = request.get_json()
        name = data.get('name', contact.name)
        email = data.get('email', contact.email)
        phone = data.get('phone', contact.phone)
        
        contact.name = name
        contact.email = email
        contact.phone = phone
        
        db.session.commit()
        
        return jsonify({'message': 'contacto actualizado con éxito', 'contact': contact.serialize()}), 200


@app.route("/contacts/<int:id>", methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.filter_by(id=id).first()
    
    if contact:
        db.session.delete(contact)
        db.session.commit()
        return jsonify({'message': 'contacto eliminado con éxito'}), 200
    
    else:
        return jsonify({'message': 'contacto no encontrado'}), 404


if __name__ == '__main__':
    app.run(port=8000)