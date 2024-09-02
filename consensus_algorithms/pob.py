import hashlib
import random

class PoB:
    def __init__(self):
        self.burned_coins = {}

    def burn_coin(self, user, amount):
        if user in self.burned_coins:
            self.burned_coins[user] += amount
        else:
            self.burned_coins[user] = amount

    def proof_of_burn(self, last_proof):
        total_burned = sum(self.burned_coins.values())
        if total_burned == 0:
            raise ValueError("No coins burned to choose from.")
        chosen_burn = random.uniform(0, total_burned)
        current = 0
        for user, amount in self.burned_coins.items():
            current += amount
            if current >= chosen_burn:
                return user, last_proof + 1

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
