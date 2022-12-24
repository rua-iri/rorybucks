import block


class Blockchain:



    def __init__(self):
        self.chain = []
        self.currentTransactions = []
        self.nodes = set()
        self.makeGenesis()



    #function to create the genesis block in the chain
    def makeGenesis(self):
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
    def checkValid(bloc, prevBloc):
        
        if prevBloc.index+1 != bloc.index:
            return False
        elif prevBloc.calcHash != bloc.calcHash:
            return False
        elif not Blockchain.verifyProof(bloc.proof, prevBloc.proof):
            return False
        elif bloc.tmeStamp <= prevBloc.tmeStamp:
            return False
        
        return True




