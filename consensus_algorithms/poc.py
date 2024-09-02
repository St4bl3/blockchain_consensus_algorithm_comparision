import random

class PoC:
    def __init__(self):
        self.capacity_providers = {}

    def add_capacity(self, user, capacity):
        if user in self.capacity_providers:
            self.capacity_providers[user] += capacity
        else:
            self.capacity_providers[user] = capacity

    def proof_of_capacity(self, last_proof):
        total_capacity = sum(self.capacity_providers.values())
        if total_capacity == 0:
            raise ValueError("No capacity available to choose from.")
        chosen_capacity = random.uniform(0, total_capacity)
        current = 0
        for user, capacity in self.capacity_providers.items():
            current += capacity
            if current >= chosen_capacity:
                return user, last_proof + 1
