from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

class Miner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    minername = db.Column(db.String(80), unique=True, nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(80), nullable=False)
    receiver = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    consensus_algo = db.Column(db.String(20), nullable=False)  # To distinguish which algorithm's transaction

class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transactions = db.Column(db.Text, nullable=False)  # Store transactions as JSON
    previous_hash = db.Column(db.String(64), nullable=False)
    proof = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.String(20), nullable=False)
    consensus_algo = db.Column(db.String(20), nullable=False)
