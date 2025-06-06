from datetime import datetime
from . import db

class Client(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    client_code = db.Column(db.String(50), nullable=False, unique=True)
    
    contacts = db.relationship(
        'Contact',
        secondary='client_contact',
        back_populates='clients'
    )
    # generated error on the sample SQLAlchemy will auto assign
   # def __init__(self, name, client_code):
      #  self.name = name
      #  self.client_code = client_code
        # client_code will be set after uniqueness check in service/controller

    @staticmethod
    def generate_initials(client_name):
        words = client_name.upper().split()
        initials = ''.join([word[0] for word in words])[:3]
        while len(initials) < 3:
            initials += 'A'
        return initials