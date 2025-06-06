from datetime import datetime
from . import db

class Contact(db.Model):
    __tablename__ = 'contact'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True) # <-- This will make sure the email is unique!
  

    clients = db.relationship(
        'Client',
        secondary='client_contact',
        back_populates='contacts'
    )

    def __init__(self, name, surname, email):
        self.name = name
        self.surname = surname
        self.email = email