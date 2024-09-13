from flask import Blueprint, request, jsonify
from app.models import Contact
from app.extensions import db

contact_bp = Blueprint("contact", __name__)


@contact_bp.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    return jsonify({"contacts": [contact.serialize() for contact in contacts]})


@contact_bp.route("/contacts", methods=["POST"])
def create_contact():
    data = request.get_json()
    name = data["name"]
    email = data["email"]
    phone = data["phone"]

    new_contact = Contact(name=name, email=email, phone=phone)

    existing_contact = Contact.query.filter_by(email=email).first()

    if existing_contact:
        return jsonify({"message": "Ya hay un contacto con este email"}), 409
    else:
        db.session.add(new_contact)
        db.session.commit()
        return (
            jsonify(
                {
                    "message": "Contacto creado con éxito",
                    "contact": new_contact.serialize(),
                }
            ),
            201,
        )


@contact_bp.route("/contacts/<int:id>", methods=["GET"])
def get_contact(id):
    contact = Contact.query.filter_by(id=id).first()

    if not contact:
        return jsonify({"message": "Contacto no encontrado"}), 404

    return jsonify({"contact": contact.serialize()}), 200


@contact_bp.route("/contacts/<int:id>", methods=["PATCH"])
def update_contact(id):
    contact = Contact.query.get_or_404(id)

    data = request.get_json()
    contact.name = data.get("name", contact.name)
    contact.email = data.get("email", contact.email)
    contact.phone = data.get("phone", contact.phone)

    db.session.commit()

    return (
        jsonify(
            {
                "message": "Contacto actualizado con éxito",
                "contact": contact.serialize(),
            }
        ),
        200,
    )


@contact_bp.route("/contacts/<int:id>", methods=["DELETE"])
def delete_contact(id):
    contact = Contact.query.filter_by(id=id).first()

    if contact:
        db.session.delete(contact)
        db.session.commit()
        return jsonify({"message": "Contacto eliminado con éxito"}), 200

    else:
        return jsonify({"message": "Contacto no encontrado"}), 404
