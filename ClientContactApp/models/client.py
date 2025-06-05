from datetime import datetime
from . import db

class Client(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    client_code = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    contacts = db.relationship(
        'Contact',
        secondary='client_contact',
        back_populates='clients'
    )

    def __init__(self, name):
        self.name = name
        # client_code will be set after uniqueness check in service/controller

    @staticmethod
    def generate_initials(client_name):
        words = client_name.upper().split()
        initials = ''.join([word[0] for word in words])[:3]
        while len(initials) < 3:
            initials += 'A'
        return initials