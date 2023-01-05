
#class to store all elements of a transaction
class Transaction:

    def __init__(self, sender, recipient, quantity):
        self.sender = sender
        self.recipient = recipient
        self.quantity = quantity

    def toString(self):
        return str(self.sender) + " -> " + str(self.recipient) + " $" + str(self.quantity)