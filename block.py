import hashlib
import time

class Block:

    def __init__(self, index, proof, prevHash, transaction, tmeStamp=None):
        self.index = index
        self.proof = proof
        self.prevHash = prevHash
        self.transaction = transaction

        #check that timestamp is not None
        if tmeStamp:
            self.tmeStamp = tmeStamp
        else:
            self.tmeStamp = time.time()

    
    #function to calculate the hash for the next block
    @property
    def calcHash(self):
        totalStr = "{}{}{}{}{}".format(self.index, self.proof, self.prevHash, self.transaction, self.tmeStamp)
        return hashlib.sha256(totalStr.encode())

    
    def __repr__(self):
        blockString = "{} - {} - {} - {} - {}".format(self.index, self.proof, self.prevHash, self.transaction, self.tmeStamp)
        return blockString