import random

class PoA:
    def __init__(self):
        self.authorities = []

    def add_authority(self, authority):
        self.authorities.append(authority)

    def proof_of_authority(self, last_proof):
        if not self.authorities:
            raise ValueError("No authorities available to choose from.")
        chosen_authority = random.choice(self.authorities)
        return chosen_authority, last_proof + 1
