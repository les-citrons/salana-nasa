
import bisect

class BankAccount:
    def __init__(self):
        self.balance = 100.0
        self.bet_value = 0
        self.seed_count = 0
        self.number_collection = {"default": [0]}
    
    def transact(self, value):
        value = round(value, 2)
        self.balance += value

    def create_collection(self, name):
        self.number_collection[name] = []

    def merge_collection(self, what, into):
        self.number_collection[into] += self.number_collection[what]
        del self.number_collection[what]
        self.number_collection[into].sort()

    def remove_collection(self, name):
        if name != "default":
            self.merge_collection(name, "default")

    def remove_number(self, collection_name, number):
        if number in self.number_collection[collection_name]:
            self.number_collection[collection_name].remove(number)

    def add_number(self, collection_name, number):
        bisect.insort(self.number_collection[collection_name], number)

    def bet(self):
        if not hasattr(self, 'bet_value'):
            self.bet_value = 0
        return self.bet_value

    def seeds(self):
        if not hasattr(self, 'seed_count'):
            self.seed_count = 0
        return self.seed_count
