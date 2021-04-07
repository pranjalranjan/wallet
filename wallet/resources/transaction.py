import sqlite3
import json
from flask_restful import Resource, reqparse
from models.transaction import TransactionModel

class Transaction(Resource):
    parser = reqparse.RequestParser()

    def get(self, wallet_id):
        transaction = TransactionModel.find_by_walletid(wallet_id)

        if transaction:
            return json.dumps(transaction)
        return {'err': 'There are no transactions associated with this wallet'}, 404

        