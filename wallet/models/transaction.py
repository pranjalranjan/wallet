from db import db

class TransactionModel(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Float(precision=2))
    timestamp = db.Column(db.String(20))
    
    wallet_id = db.Column(db.String(20), db.ForeignKey('wallet.id'))
    wallet = db.relationship('WalletModel')

    def __init__(self, amount, timestamp, wallet_id):
        self.amount = amount
        self.timestamp = timestamp
        self.wallet_id = wallet_id
    
    def json(self):
        return {'amount': self.id, 'timestamp': self.timestamp}
    
    @classmethod
    def find_by_walletid(cls, wallet_id):
        return TransactionModel.query.filter_by(wallet_id=wallet_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_delete(self):
        db.session.delete(self)
        db.session.commit()