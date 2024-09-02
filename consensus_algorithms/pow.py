import hashlib
import json
import time

class PoW:
    def __init__(self):
        self.blockchain = []

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.blockchain) + 1,
            'timestamp': str(time.time()),
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.blockchain[-1]),
        }
        self.blockchain.append(block)
        return block

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    @staticmethod
    def hash(block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self):
        previous_block = self.blockchain[0]
        block_index = 1
        while block_index < len(self.blockchain):
            block = self.blockchain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
