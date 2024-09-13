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
    db.session.add(new_contact)
    db.session.commit()
    
    return jsonify(
        {
            'message': 'contacto creado con éxito', 
            'contact': new_contact.serialize()
        }
        )




if __name__ == '__main__':
    app.run(port=8000)