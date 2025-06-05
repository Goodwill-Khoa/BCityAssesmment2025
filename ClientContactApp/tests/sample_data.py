from app import app
from models import db
from models.client import Client
from models.contact import Contact

with app.app_context():
    # Wipe old data
    db.drop_all()
    db.create_all()

    # Create sample contacts
    contact1 = Contact(name='Alice Smith', email='alice@example.com', phone='123-456-7890')
    contact2 = Contact(name='Bob Johnson', email='bob@example.com', phone='234-567-8901')
    contact3 = Contact(name='Carol Lee', email='carol@example.com', phone='345-678-9012')
    db.session.add_all([contact1, contact2, contact3])
    db.session.commit()

    # Create sample clients, some linked to contacts
    client1 = Client(name='Acme Corp', code='ACME', contact_id=contact1.id)
    client2 = Client(name='Globex Inc', code='GLOB', contact_id=contact2.id)
    client3 = Client(name='Soylent Co', code='SOYL', contact_id=None)  # Unlinked client
    client4 = Client(name='Initech', code='INIT', contact_id=contact3.id)
    db.session.add_all([client1, client2, client3, client4])
    db.session.commit()

    print("Sample data inserted!")