from app import create_app
from models import db
from models.client import Client
from models.contact import Contact
from models.client_contact import ClientContact

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Sample Clients
    client1 = Client(name='Acme Corporation', client_code='ACA001')
    client2 = Client(name='Globex Inc.', client_code='GIA001')
    client3 = Client(name='Initech', client_code='INI001')
    db.session.add_all([client1, client2, client3])
    db.session.commit()

    # Sample Contacts
    contact1 = Contact(name='Alice', surname='Smith', email='alice.smith@example.com')
    contact2 = Contact(name='Bob', surname='Johnson', email='bob.johnson@example.com')
    contact3 = Contact(name='Carol', surname='Williams', email='carol.williams@example.com')
    contact4 = Contact(name='David', surname='Brown', email='david.brown@example.com')
    db.session.add_all([contact1, contact2, contact3, contact4])
    db.session.commit()

    # Sample Links (Many-to-Many)
    link1 = ClientContact(client_id=client1.id, contact_id=contact1.id)
    link2 = ClientContact(client_id=client1.id, contact_id=contact2.id)
    link3 = ClientContact(client_id=client2.id, contact_id=contact2.id)
    link4 = ClientContact(client_id=client2.id, contact_id=contact3.id)
    link5 = ClientContact(client_id=client3.id, contact_id=contact4.id)
    db.session.add_all([link1, link2, link3, link4, link5])
    db.session.commit()

    print("Sample data inserted!")