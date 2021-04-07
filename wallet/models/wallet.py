from db import db

class WalletModel(db.Model):
    __tablename__ = 'wallet'

    id = db.Column(db.String(20), primary_key=True)
    balance = db.Column(db.Float(precision=2))

    transactions = db.relationship('TransactionModel')

    def __init__(self, id, balance):
        self.id = id
        self.balance = balance
    
    def json(self):
        return {'id': self.id, 'balance': self.balance, 'transactions': [transaction.json() for transaction in self.transactions]}
    
    @classmethod
    def find_by_id(cls, id):
        return WalletModel.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_delete(self):
        db.session.delete(self)
        db.session.commit()