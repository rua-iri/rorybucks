import hashlib
import block
import transaction


class Blockchain:



    def __init__(self):
        self.chain = []
        self.currentTransactions = []
        self.nodes = set()
        self.makeGenesis()



    #function to create the genesis block in the chain
    def makeGenesis(self):
        self.addTransaction(0, 0, 0)
        self.makeBlock(proof=0, prevHash=0)



    #function to add another block to the blockchain
    def makeBlock(self, proof, prevHash):

        #instantiate a new block
        bloc = block.Block(
            index=len(self.chain),
            proof=proof,
            prevHash=prevHash,
            transaction=self.currentTransactions
            )
        
        #reset current transactions
        self.currentTransactions = []

        self.chain.append(bloc)
        return bloc



    #check that each block correctly points to the previous block's hash
    @staticmethod
    def checkValid(bloc, prevBloc):
        
        if prevBloc.index+1 != bloc.index:
            return False
        elif prevBloc.calcHash != bloc.calcHash:
            return False
        elif not Blockchain.verifyProof(prevBloc.proof, bloc.proof):
            return False
        elif bloc.tmeStamp <= prevBloc.tmeStamp:
            return False
        
        return True


    #function to add a new transaction to the chain
    def addTransaction(self, sendr, receiver, amount):
        transact = transaction.Transaction(sendr, receiver, amount)
        self.currentTransactions.append(transact)

        return True



    @staticmethod
    def proofOfWork(prevProof):
        proofNum = 0

        #increment proofNum until verifyProof returns True
        while Blockchain.verifyProof(prevProof, proofNum) is False:
            proofNum+=1
        
        return proofNum



    #determine if proof is valid
    @staticmethod
    def verifyProof(prevProof, proof):
        guess = f'{prevProof}{proof}'.encode()
        guessHash = hashlib.sha256(guess).hexdigest()

        #return true if first four chars are 0000
        return guessHash[:4] == "0000"



    #return the most recent block in the chain
    @property
    def lastBlock(self):
        return self.chain[-1]
