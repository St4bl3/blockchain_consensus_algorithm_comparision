from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, User, Miner, Transaction, Block
from consensus_algorithms.pow import PoW
from consensus_algorithms.pos import PoS
from consensus_algorithms.dpos import DPoS
from consensus_algorithms.poa import PoA
from consensus_algorithms.poc import PoC
from consensus_algorithms.pob import PoB
import json
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blockchain.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize consensus algorithm instances
pow_instance = PoW()
pos_instance = PoS()
dpos_instance = DPoS()
poa_instance = PoA()
poc_instance = PoC()
pob_instance = PoB()

with app.app_context():
    db.create_all()

def get_transactions(consensus_algo):
    return Transaction.query.filter_by(consensus_algo=consensus_algo).all()

def get_blocks(consensus_algo):
    return Block.query.filter_by(consensus_algo=consensus_algo).all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/pow')
def pow_page():
    users = User.query.all()
    miners = Miner.query.all()
    transactions = get_transactions('pow')
    blocks = get_blocks('pow')
    return render_template('pow.html', users=users, miners=miners, transactions=transactions, blocks=blocks)

@app.route('/pos')
def pos_page():
    users = User.query.all()
    miners = Miner.query.all()
    transactions = get_transactions('pos')
    blocks = get_blocks('pos')
    return render_template('pos.html', users=users, miners=miners, transactions=transactions, blocks=blocks)

@app.route('/dpos')
def dpos_page():
    users = User.query.all()
    miners = Miner.query.all()
    transactions = get_transactions('dpos')
    blocks = get_blocks('dpos')
    return render_template('dpos.html', users=users, miners=miners, transactions=transactions, blocks=blocks)

@app.route('/poa')
def poa_page():
    users = User.query.all()
    miners = Miner.query.all()
    transactions = get_transactions('poa')
    blocks = get_blocks('poa')
    return render_template('poa.html', users=users, miners=miners, transactions=transactions, blocks=blocks)

@app.route('/poc')
def poc_page():
    users = User.query.all()
    miners = Miner.query.all()
    transactions = get_transactions('poc')
    blocks = get_blocks('poc')
    return render_template('poc.html', users=users, miners=miners, transactions=transactions, blocks=blocks)

@app.route('/pob')
def pob_page():
    users = User.query.all()
    miners = Miner.query.all()
    transactions = get_transactions('pob')
    blocks = get_blocks('pob')
    return render_template('pob.html', users=users, miners=miners, transactions=transactions, blocks=blocks)

# Routes for adding users, miners, and transactions
@app.route('/pow/add_user', methods=['POST'])
def add_pow_user():
    username = request.form['username']
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('pow_page'))

@app.route('/pow/add_miner', methods=['POST'])
def add_pow_miner():
    minername = request.form['minername']
    miner = Miner(minername=minername)
    db.session.add(miner)
    db.session.commit()
    return redirect(url_for('pow_page'))

@app.route('/pow/add_transaction', methods=['POST'])
def add_pow_transaction():
    sender = request.form['sender']
    receiver = request.form['receiver']
    amount = request.form['amount']

    # Check if sender and receiver exist in the database
    if not User.query.filter_by(username=sender).first() or not User.query.filter_by(username=receiver).first():
        return redirect(url_for('pow_page'))  # Transaction invalid

    transaction = Transaction(sender=sender, receiver=receiver, amount=amount, consensus_algo='pow')
    db.session.add(transaction)
    db.session.commit()

    # Check if the number of transactions reached 5
    transactions = get_transactions('pow')
    if len(transactions) >= 5:
        previous_block = Block.query.filter_by(consensus_algo='pow').order_by(Block.id.desc()).first()
        previous_hash = previous_block.previous_hash if previous_block else '0'
        proof = pow_instance.proof_of_work(previous_block.proof if previous_block else 1)
        block = Block(transactions=json.dumps([t.id for t in transactions[:5]]),
                      previous_hash=previous_hash, proof=proof, timestamp=str(time.time()), consensus_algo='pow')
        db.session.add(block)
        db.session.commit()
        # Remove the transactions that were included in the block
        for t in transactions[:5]:
            db.session.delete(t)
        db.session.commit()

    return redirect(url_for('pow_page'))

@app.route('/pos/add_user', methods=['POST'])
def add_pos_user():
    username = request.form['username']
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('pos_page'))

@app.route('/pos/add_miner', methods=['POST'])
def add_pos_miner():
    minername = request.form['minername']
    miner = Miner(minername=minername)
    db.session.add(miner)
    db.session.commit()
    return redirect(url_for('pos_page'))

@app.route('/pos/add_transaction', methods=['POST'])
def add_pos_transaction():
    sender = request.form['sender']
    receiver = request.form['receiver']
    amount = request.form['amount']

    # Check if sender and receiver exist in the database
    if not User.query.filter_by(username=sender).first() or not User.query.filter_by(username=receiver).first():
        return redirect(url_for('pos_page'))  # Transaction invalid

    transaction = Transaction(sender=sender, receiver=receiver, amount=amount, consensus_algo='pos')
    db.session.add(transaction)
    db.session.commit()

    # Check if the number of transactions reached 5
    transactions = get_transactions('pos')
    if len(transactions) >= 5:
        previous_block = Block.query.filter_by(consensus_algo='pos').order_by(Block.id.desc()).first()
        previous_hash = previous_block.previous_hash if previous_block else '0'
        proof = pos_instance.proof_of_stake(previous_block.proof if previous_block else 1)
        block = Block(transactions=json.dumps([t.id for t in transactions[:5]]),
                      previous_hash=previous_hash, proof=proof, timestamp=str(time.time()), consensus_algo='pos')
        db.session.add(block)
        db.session.commit()
        # Remove the transactions that were included in the block
        for t in transactions[:5]:
            db.session.delete(t)
        db.session.commit()

    return redirect(url_for('pos_page'))

@app.route('/dpos/add_user', methods=['POST'])
def add_dpos_user():
    username = request.form['username']
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('dpos_page'))

@app.route('/dpos/add_miner', methods=['POST'])
def add_dpos_miner():
    minername = request.form['minername']
    miner = Miner(minername=minername)
    db.session.add(miner)
    db.session.commit()
    return redirect(url_for('dpos_page'))

@app.route('/dpos/add_transaction', methods=['POST'])
def add_dpos_transaction():
    sender = request.form['sender']
    receiver = request.form['receiver']
    amount = request.form['amount']

    # Check if sender and receiver exist in the database
    if not User.query.filter_by(username=sender).first() or not User.query.filter_by(username=receiver).first():
        return redirect(url_for('dpos_page'))  # Transaction invalid

    transaction = Transaction(sender=sender, receiver=receiver, amount=amount, consensus_algo='dpos')
    db.session.add(transaction)
    db.session.commit()

    # Check if the number of transactions reached 5
    transactions = get_transactions('dpos')
    if len(transactions) >= 5:
        previous_block = Block.query.filter_by(consensus_algo='dpos').order_by(Block.id.desc()).first()
        previous_hash = previous_block.previous_hash if previous_block else '0'
        proof = dpos_instance.delegated_proof_of_stake(previous_block.proof if previous_block else 1)
        block = Block(transactions=json.dumps([t.id for t in transactions[:5]]),
                      previous_hash=previous_hash, proof=proof, timestamp=str(time.time()), consensus_algo='dpos')
        db.session.add(block)
        db.session.commit()
        # Remove the transactions that were included in the block
        for t in transactions[:5]:
            db.session.delete(t)
        db.session.commit()

    return redirect(url_for('dpos_page'))

@app.route('/poa/add_user', methods=['POST'])
def add_poa_user():
    username = request.form['username']
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('poa_page'))

@app.route('/poa/add_miner', methods=['POST'])
def add_poa_miner():
    minername = request.form['minername']
    miner = Miner(minername=minername)
    db.session.add(miner)
    db.session.commit()
    return redirect(url_for('poa_page'))

@app.route('/poa/add_transaction', methods=['POST'])
def add_poa_transaction():
    sender = request.form['sender']
    receiver = request.form['receiver']
    amount = request.form['amount']

    # Check if sender and receiver exist in the database
    if not User.query.filter_by(username=sender).first() or not User.query.filter_by(username=receiver).first():
        return redirect(url_for('poa_page'))  # Transaction invalid

    transaction = Transaction(sender=sender, receiver=receiver, amount=amount, consensus_algo='poa')
    db.session.add(transaction)
    db.session.commit()

    # Check if the number of transactions reached 5
    transactions = get_transactions('poa')
    if len(transactions) >= 5:
        previous_block = Block.query.filter_by(consensus_algo='poa').order_by(Block.id.desc()).first()
        previous_hash = previous_block.previous_hash if previous_block else '0'
        proof = poa_instance.proof_of_authority(previous_block.proof if previous_block else 1)
        block = Block(transactions=json.dumps([t.id for t in transactions[:5]]),
                      previous_hash=previous_hash, proof=proof, timestamp=str(time.time()), consensus_algo='poa')
        db.session.add(block)
        db.session.commit()
        # Remove the transactions that were included in the block
        for t in transactions[:5]:
            db.session.delete(t)
        db.session.commit()

    return redirect(url_for('poa_page'))

@app.route('/poc/add_user', methods=['POST'])
def add_poc_user():
    username = request.form['username']
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('poc_page'))

@app.route('/poc/add_miner', methods=['POST'])
def add_poc_miner():
    minername = request.form['minername']
    miner = Miner(minername=minername)
    db.session.add(miner)
    db.session.commit()
    return redirect(url_for('poc_page'))

@app.route('/poc/add_transaction', methods=['POST'])
def add_poc_transaction():
    sender = request.form['sender']
    receiver = request.form['receiver']
    amount = request.form['amount']

    # Check if sender and receiver exist in the database
    if not User.query.filter_by(username=sender).first() or not User.query.filter_by(username=receiver).first():
        return redirect(url_for('poc_page'))  # Transaction invalid

    transaction = Transaction(sender=sender, receiver=receiver, amount=amount, consensus_algo='poc')
    db.session.add(transaction)
    db.session.commit()

    # Check if the number of transactions reached 5
    transactions = get_transactions('poc')
    if len(transactions) >= 5:
        previous_block = Block.query.filter_by(consensus_algo='poc').order_by(Block.id.desc()).first()
        previous_hash = previous_block.previous_hash if previous_block else '0'
        proof = poc_instance.proof_of_capacity(previous_block.proof if previous_block else 1)
        block = Block(transactions=json.dumps([t.id for t in transactions[:5]]),
                      previous_hash=previous_hash, proof=proof, timestamp=str(time.time()), consensus_algo='poc')
        db.session.add(block)
        db.session.commit()
        # Remove the transactions that were included in the block
        for t in transactions[:5]:
            db.session.delete(t)
        db.session.commit()

    return redirect(url_for('poc_page'))

@app.route('/pob/add_user', methods=['POST'])
def add_pob_user():
    username = request.form['username']
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('pob_page'))

@app.route('/pob/add_miner', methods=['POST'])
def add_pob_miner():
    minername = request.form['minername']
    miner = Miner(minername=minername)
    db.session.add(miner)
    db.session.commit()
    return redirect(url_for('pob_page'))

@app.route('/pob/add_transaction', methods=['POST'])
def add_pob_transaction():
    sender = request.form['sender']
    receiver = request.form['receiver']
    amount = request.form['amount']

    # Check if sender and receiver exist in the database
    if not User.query.filter_by(username=sender).first() or not User.query.filter_by(username=receiver).first():
        return redirect(url_for('pob_page'))  # Transaction invalid

    transaction = Transaction(sender=sender, receiver=receiver, amount=amount, consensus_algo='pob')
    db.session.add(transaction)
    db.session.commit()

    # Check if the number of transactions reached 5
    transactions = get_transactions('pob')
    if len(transactions) >= 5:
        previous_block = Block.query.filter_by(consensus_algo='pob').order_by(Block.id.desc()).first()
        previous_hash = previous_block.previous_hash if previous_block else '0'
        proof = pob_instance.proof_of_burn(previous_block.proof if previous_block else 1)
        block = Block(transactions=json.dumps([t.id for t in transactions[:5]]),
                      previous_hash=previous_hash, proof=proof, timestamp=str(time.time()), consensus_algo='pob')
        db.session.add(block)
        db.session.commit()
        # Remove the transactions that were included in the block
        for t in transactions[:5]:
            db.session.delete(t)
        db.session.commit()

    return redirect(url_for('pob_page'))

if __name__ == '__main__':
    app.run(debug=True)
