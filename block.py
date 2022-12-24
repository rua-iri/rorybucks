import hashlib
import time

class Block:

    def __init__(self, index, proof, prevHash, data, tmeStamp=None):
        self.index = index
        self.proof = proof
        self.prevHash = prevHash
        self.data = data

        #check that timestamp is not None
        if tmeStamp:
            self.tmeStamp = tmeStamp
        else:
            self.tmeStamp = time.time()

    
    #function to calculate the hash for the next block
    def calcHash(self):
        totalStr = "{}{}{}{}{}".format(self.index, self.proof, self.prevHash, self.data, self.tmeStamp)
        return hashlib.sha256(totalStr.encode())

    
    def __repr__(self):
        blockString = "{} - {} - {} - {} - {}".format(self.index, self.proof, self.prevHash, self.data, self.tmeStamp)
        return blockString