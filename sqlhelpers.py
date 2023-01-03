import app
import block
import blockchain


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

            for clmn in self.columnsList:
                createData += "%s varchar(100)," %clmn
 
            cur =  app.mySql.connection.cursor()
            print("CREATE TABLE %s(%s)" %(self.table, createData[:len(createData)-1]))
            cur.execute("CREATE TABLE %s(%s)" %(self.table, createData[:len(createData)-1]))
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

    def insert(self, *args):
        data = ""
        
        for arg in args:
            data += "\"%s\"," %(arg)

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
    users = Table("users", "name", "email", "username", "password")
    data = users.getAll()
    usernames = [user.get("username") for user in data]

    return False if username in usernames else True



def sendBucks(sendr, receivr, amount):

    #check that amount is sufficient
    try:
        amount = float(amount)
    except:
        raise InvalidTransactionError("Invalid Transaction")
    

    if amount > getBalance() and sendr!="THEBOSS":
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




def getBalance():
    balan = 0.00
    bChain = getBlockchain()



def getBlockchain():
    bChain = blockchain.Blockchain()
    bChainSql = Table("blockchain", "number", "hash", "previous", "data", "nonce")

    for blk in bChainSql.getAll():
        bChain.makeBlock(blk.get("previous"), blk.get("nonce"))


def syncBlockchain(bChain):
    bChainSql = Table("blockchain", "number", "hash", "previous", "data", "nonce")
    bChainSql.deleteAll()

    for blck in bChain.chain:
        if blck.index>0:
            bChainSql.insert(str(blck.index), blck.calcHash, blck.prevHash, blck.transaction[0].toString(), blck.proof)
        else:
            bChainSql.insert(str(blck.index), blck.calcHash, blck.prevHash, blck.transaction, blck.proof)
        



