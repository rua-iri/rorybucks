import app
import blockchain
import sqlqueries


class InvalidTransactionError(Exception):
    pass

class InsufficientFundsException(Exception):
    pass


class Table():
    
    def __init__(self, tableName, *args):
        self.table = tableName
        self.columns = "(%s)" %",".join(args)
        self.columnsList = args

        if isNewTable(tableName):
            createData = ""
            createStatement = ""

            if self.table=="blockchain":
                createStatement = sqlqueries.createBlockchain
            elif self.table=="transactions":
                createStatement = sqlqueries.createTransactions
            elif self.table=="users":
                #TODO add create users query
                createStatement = ""
            

 
            cur =  app.mySql.connection.cursor()
            cur.execute(createStatement)
            cur.close()


    def getAll(self):
        cur = app.mySql.connection.cursor()
        res = cur.execute("SELECT * FROM %s" %self.table)
        data = cur.fetchall()
        return data

    def getOne(self, search, value):
        data = {}
        cur = app.mySql.connection.cursor()
        result = cur.execute("SELECT * FROM %s WHERE %s = \"%s\"" %(self.table, search, value))

        if result>0:
            data = cur.fetchone()

        cur.close()
        return data

    def getLast(self, idName):
        cur = app.mySql.connection.cursor()
        res = cur.execute("SELECT * FROM %s ORDER BY %s DESC LIMIT 1" %(self.table, idName))
        data = cur.fetchone()
        return data


    def deleteOne(self, search, value):
        cur = app.mySql.connection.cursor()
        cur.execute("DELETE FROM %s WHERE %s = \"%s\"" %(self.table, search, value))
        app.mySql.connection.commit()
        cur.close()
    
    def deleteAll(self):
        self.drop()
        self.__init__(self.table, *self.columnsList)

    def drop(self):
        cur = app.mySql.connection.cursor()
        cur.execute("SET foreign_key_checks = 0;")
        cur.execute("DROP TABLE %s" %self.table)
        cur.execute("SET foreign_key_checks = 1;")
        cur.close()

    def insert(self, *args):
        data = ""
        
        #Don't put quotation marks around null values
        for arg in args:
            if arg=="null":
                data += "%s," %(arg)
            else:
                data += "\"%s\"," %(arg)

        #TODO remove this, just for testing
        print("\n")
        print(("INSERT INTO %s%s VALUES(%s)" %(self.table, self.columns, data[:len(data)-1])))
        print("\n")

        cur = app.mySql.connection.cursor()
        cur.execute("INSERT INTO %s%s VALUES(%s)" %(self.table, self.columns, data[:len(data)-1]))
        app.mySql.connection.commit()
        cur.close()


def sqlRaw(execution):
    cur = app.mySql.connection.cursor()
    cur.execute(execution)
    app.mySql.connection.commit()
    cur.close()


def isNewTable(tableName):
    cur =  app.mySql.connection.cursor()

    try:
        result = cur.execute("SELECT * FROM %s" %tableName)
        cur.close()

    except:
        return True

    else:
        return False


def isNewUser(username):
    users = Table("users", "user_id", "name", "username", "email", "password", "balance")
    data = users.getAll()
    usernames = [user.get("username") for user in data]

    return False if username in usernames else True



def sendBucks(sendr, receivr, amount):

    #check that amount is sufficient
    try:
        amount = float(amount)
    except:
        raise InvalidTransactionError("Invalid Transaction")

    sendrBal = getBalance(sendr)
    
    if sendrBal==None:
        sendrBal = 0
    

    if amount > sendrBal and sendr!="THEBOSS":
        raise InsufficientFundsException("Insufficient Funds")
    elif sendr==receivr or amount<=0:
        raise InvalidTransactionError("Invalid Transaction")
    elif isNewUser(receivr):
        raise InvalidTransactionError("User Does Not Exist")

    #if valid, add transaction to blockchain
    bChain = getBlockchain()

    lBlock = bChain.lastBlock
    lProof = lBlock.proof
    proofNum = bChain.proofOfWork(lProof)
    bChain.addTransaction(sendr, receivr, amount)
    lHash = lBlock.calcHash
    bChain.makeBlock(proofNum, lHash)

    #TODO subtract amount sent from the sender's balance

    for blk in bChain.chain:
        print(blk)

    syncBlockchain(bChain)




#function to check a user's balance in the db
def getBalance(uName):

    userSQL = Table("users", "user_id", "name", "username", "email", "password", "balance")
    userToCheck = userSQL.getOne("username", uName)
    userBal = userToCheck.get("balance")

    return userBal



def getBlockchain():
    bChain = blockchain.Blockchain()
    bChainSql = Table("blockchain", "block_id", "hash", "prev_hash", "transaction_id", "proof")

    for blk in bChainSql.getAll():
        bChain.makeBlock(blk.get("prev_hash"), blk.get("proof"))
    
    return bChain




def syncBlockchain(bChain):
    bChainSql = Table("blockchain", "block_id", "hash", "prev_hash", "transaction_id", "proof")
    # bChainSql.deleteAll()
    transactionSql = Table("transactions", "transaction_id", "sender", "recipient", "amount")
    # transactionSql.deleteAll()
    userSql = Table("users", "user_id", "name", "username", "email", "password", "balance")


    #iterate through each block in the chain
    for blck in bChain.chain:

        print(blck.index)
        print(blck)
        print(len(blck.transaction))

        #alter insertion slightly only for the genesis block
        if len(blck.transaction)>0:

            #get the user_id for the sender and recipient
            sendrUser = userSql.getOne("username", blck.transaction[0].sender)
            senderId = sendrUser.get("user_id")
            receiveUser = userSql.getOne("username", blck.transaction[0].recipient)
            recieveId = receiveUser.get("user_id")

            print("\n\n")
            print(blck.transaction[0].sender)
            print(blck.transaction[0].recipient)
            print("\n\n")

            
            transactionSql.insert("null", senderId, recieveId, blck.transaction[0].quantity)
            transactionData = transactionSql.getLast("transaction_id")
            print(transactionData)

            bChainSql.insert("null", blck.calcHash, blck.prevHash, transactionData.get("transaction_id"), blck.proof)

        else:
            bChainSql.insert("null", blck.calcHash, blck.prevHash, 1, blck.proof)
        



