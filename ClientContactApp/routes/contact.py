from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from models import db
from models.client import Client
from models.contact import Contact
import re   #for email validation

contact_bp = Blueprint('contact', __name__, url_prefix='/contacts')

#simple validation rule for email
def is_valid_email(email):
    # Simple regex for demonstration
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

@contact_bp.route('/')
def list_contacts():
    contacts = Contact.query.order_by(Contact.surname, Contact.name).all()
    return render_template('contact_list.html', contacts=contacts)

@contact_bp.route('/create', methods=['GET', 'POST'])
def create_contact():
    if request.method == 'POST':
        name = request.form['name'].strip()
        surname = request.form['surname'].strip()
        email = request.form['email'].strip()

        # : Email format validation ---
        if not is_valid_email(email):
            flash('Invalid email address.', 'error')
            return render_template('contact_form.html')
        
        if not name or not surname or not email:
            return render_template('contact_form.html', error="All fields are required.")
        # Email uniqueness check
        if Contact.query.filter_by(email=email).first():
            return render_template('contact_form.html', error="Email already exists.")
        contact = Contact(name=name, surname=surname, email=email)
        db.session.add(contact)
        db.session.commit()
        return redirect(url_for('contact.view_contact', contact_id=contact.id))
    return render_template('contact_form.html')

@contact_bp.route('/<int:contact_id>')
def view_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    linked_clients = contact.clients
    return render_template('contact_detail.html', contact=contact, clients=linked_clients)

@contact_bp.route('/<int:contact_id>/link_client', methods=['POST'])
def link_client(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    client_id = request.form['client_id']
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'success': False, 'message': 'Client not found.'}), 404
    if client not in contact.clients:
        contact.clients.append(client)
        db.session.commit()
    return jsonify({'success': True})

@contact_bp.route('/<int:contact_id>/unlink_client', methods=['POST'])
def unlink_client(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    client_id = request.form['client_id']
    client = Client.query.get(client_id)
    if client in contact.clients:
        contact.clients.remove(client)
        db.session.commit()
    return jsonify({'success': True})

@contact_bp.route('/ajax/link_unlink_client', methods=['POST'])
def link_unlink_client_ajax():
    contact_id = request.form.get('contact_id')
    client_id = request.form.get('client_id')
    action = request.form.get('action')
    contact = Contact.query.get(contact_id)
    client = Client.query.get(client_id)
    if not contact or not client:
        return jsonify(success=False)
    if action == "link":
        if client not in contact.clients:
            contact.clients.append(client)
    elif action == "unlink":
        if client in contact.clients:
            contact.clients.remove(client)
    db.session.commit()
    return jsonify(success=True)


@contact_bp.route('/search', methods=['GET'])
def search_contact():
    name = request.args.get('name', '').strip()
    if not name:
        return jsonify({'found': False})
    # Searches by name or surname (case-insensitive)
    contact = Contact.query.filter(
        (Contact.name.ilike(f"%{name}%")) | (Contact.surname.ilike(f"%{name}%"))
    ).first()
    if contact:
        return jsonify({'found': True, 'contact_id': contact.id})
    return jsonify({'found': False})