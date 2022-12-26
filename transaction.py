
#class to store all elements of a transaction
class Transaction:

    def __init__(self, sender, recipient, quantity):
        self.sender = sender
        self.recipient = recipient
        self.quantitiy = quantity