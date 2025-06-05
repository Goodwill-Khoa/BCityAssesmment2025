from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from models import db
from models.client import Client
from models.contact import Contact
from models.client_contact import ClientContact

client_bp = Blueprint('client', __name__, url_prefix='/clients')

def generate_unique_client_code(name):
    initials = Client.generate_initials(name)
    # Find latest code with these initials
    latest = Client.query.filter(Client.client_code.like(f"{initials}%")) \
        .order_by(Client.client_code.desc()).first()
    if latest and latest.client_code[3:].isdigit():
        number = int(latest.client_code[3:]) + 1
    else:
        number = 1
    return f"{initials}{number:03}"

@client_bp.route('/')
def list_clients():
    clients = Client.query.order_by(Client.name).all()
    return render_template('client_list.html', clients=clients)

@client_bp.route('/create', methods=['GET', 'POST'])
def create_client():
    if request.method == 'POST':
        name = request.form['name'].strip()
        if not name:
            return render_template('client_form.html', error="Name is required.")
        code = generate_unique_client_code(name)
        client = Client(name=name)
        client.client_code = code
        db.session.add(client)
        db.session.commit()
        return redirect(url_for('client.view_client', client_id=client.id))
    return render_template('client_form.html')

@client_bp.route('/<int:client_id>')
def view_client(client_id):
    client = Client.query.get_or_404(client_id)
    linked_contacts = client.contacts
    return render_template('client_detail.html', client=client, contacts=linked_contacts)

@client_bp.route('/<int:client_id>/link_contact', methods=['POST'])
def link_contact(client_id):
    client = Client.query.get_or_404(client_id)
    contact_id = request.form['contact_id']
    contact = Contact.query.get(contact_id)
    if not contact:
        return jsonify({'success': False, 'message': 'Contact not found.'}), 404
    if contact not in client.contacts:
        client.contacts.append(contact)
        db.session.commit()
    return jsonify({'success': True})

@client_bp.route('/<int:client_id>/unlink_contact', methods=['POST'])
def unlink_contact(client_id):
    client = Client.query.get_or_404(client_id)
    contact_id = request.form['contact_id']
    contact = Contact.query.get(contact_id)
    if contact in client.contacts:
        client.contacts.remove(contact)
        db.session.commit()
    return jsonify({'success': True})