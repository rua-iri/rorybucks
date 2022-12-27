import app


class Table():
    
    def __init(self, tableName, *args):
        self.table = tableName
        self.columns = "(%s)" %",".join(args)
        self.columnsList = args

        if isNewTable(tableName):
            createData = ""

            for clmn in self.columnsList:
                createData += "%s varchar(100)," %clmn
 
            cur =  app.mySql.connection.cursor()
            cur.execute("CREATE TABLE %s%s" %(self.table, self.columns))
            cur.close()


    def getAll(self):
        cur = app.mySql.cursor()
        res = cur.execute("SELECT * FROM %s" %self.table)
        data = cur.fetchall()
        return data

    def getOne(self, search, value):
        pass

    def deleteOne(self, search, value):
        pass

    def drop(self):
        pass

    def insert(self, *args):
        pass




def isNewTable(tableName):
    cur =  app.mySql.connection.cursor()

    try:
        result = cur.execute("SELECT * FROM %s" %tableName)
        cur.close()

    except:
        return True

    else:
        return False

    
