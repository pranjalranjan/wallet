import sqlite3
import threading
from flask_restful import Resource, reqparse
from models.wallet import WalletModel
from models.transaction import TransactionModel
from datetime import datetime
sem = threading.Semaphore()

class Wallet(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('amount', 
        type=float,
        required=True,
        help='Amount cannot be empty'
    )

    def get(self, id):
        wallet = WalletModel.find_by_id(id)

        if wallet:
            return wallet.json()
        return {'err': 'There is no wallet associated with this id'}, 404
    
    def post(self, id):
        #Acquires lock to ensure strong consistency if multiple users try to transact
        sem.acquire()
        data = Wallet.parser.parse_args()
        wallet = WalletModel.find_by_id(id)
        print(data['amount'])

        if wallet is None:
            sem.release()
            return {'err': 'There is no wallet associated with this id'}, 404
        else:
            try:
                amount = data['amount']
                if ((amount < 0) and (wallet.balance + amount < 10.00)):
                    sem.release()
                    return {'err': 'Minimum balance of 10 must be kept in the wallet'}, 400
                wallet.balance += amount
                wallet.save_to_db()
                self.__recordTransaction(id, amount, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            except:
                sem.release()
                return {'err': 'An error occured while carrying out the transaction'}, 500
        sem.release()
        return wallet.json()

    def put(self, id):
        if WalletModel.find_by_id(id):
            return {'err': "A wallet with id '{}' already exists".format(id)}, 400
        
        data = Wallet.parser.parse_args()

        initial_funding = data['amount']
        if(initial_funding < 10.00):
            return {"err": "Wallet must be created with a minimum balance of 10"}, 400
        wallet = WalletModel(id, 0)

        try:
            wallet.save_to_db()
            self.__recordTransaction(id, amount, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        except:
            return {"err": "An error occured while creating the wallet"}, 500
        
        return wallet.json(), 201

    def __recordTransaction(self, id, amount, timestamp):
        transaction = TransactionModel(amount, timestamp, id)
        try:
            transaction.save_to_db()
        except:
            return {"err": "An error occured while recording the transaction"}
        