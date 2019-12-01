import mysql.connector
import random
'''
Things left to do
    1. TESTING SELECT FUNCTION WITH ALL SEMANTICS
    2. Add a remove 0 standard semantics statement to the Standard Semantics projection function.    
'''

# database=input("Database name in mySQL: ")
database = "production"
inputDb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    database=database
)
mycursor = inputDb.cursor()
Semantics = [("StandardSem"),  # 0
             ("BagSem"),  # 1
             ("PolynomialSem"),  # 2
             ("ProbabilitySem"),  # 3
             ("CertaintySem")]  # 4


def select(query,Semantics,TABLENAME):
    '''

    :param query:
    :param Semantics:
    :return:

    S[column1,column2,....](Table){condition1 & condition2 ^ conditon3 ...}

    '''
    #query = "S[product_id,product_name](products)|product_id<5|"
    columns = query[query.find('[') + 1:query.find(']')]
    table = query[query.find('(') + 1:query.find(')')]
    conditions= query[query.find('|')+1:len(query)-1]
    conditions=conditions.replace("&","AND")
    conditions=conditions.replace("^","OR")

    tempTable="temp"+table

    q="CREATE TABLE %s SELECT %s,%s FROM %s WHERE %s;"%(tempTable,columns,Semantics,table,conditions)
    #print(q)
    mycursor.execute(q)
    q="#[%s](%s)"%(columns,tempTable)

    print(q)
    project(q,Semantics,TABLENAME)

    q="DROP TABLE %s"%tempTable
    mycursor.execute(q)

def join(query, Semantics,TABLENAME):
    '''
        The 2 tables to be joined.
        J[table1](table2)
    '''

    table1=query[query.find('[')+1:query.find(']')]
    table2=query[query.find('(')+1:query.find(')')]

    mycursor.execute("DESCRIBE %s" %table1)
    T1Attributes =mycursor.fetchall()   #Gets all the names of the columns in Table 1
    #print(T1Attributes)

    mycursor.execute("DESCRIBE %s" %table2)
    T2Attributes =mycursor.fetchall()   #Gets all the names of the column in Table 2
    #print(T2Attributes)

    commonAttributes=[]
    Columns=""
    firstExecution=True

    #Looping through the 2 Table Attributes to find all the common Attributes, incase a join needs to happen with more than 1 column
    for i in T1Attributes:
        for j in T2Attributes:
            if i[0]==j[0] and not i[0]==Semantics :
                commonAttributes.append(i[0])
                if firstExecution==True:
                    firstExecution=False
                    Columns="%s.%s, "%(table1,i[0])
                else:
                    Columns=Columns+"%s.%s, "%(table1,i[0])

    #Looping though the Table 1 Attributes to find all the unique column names for the SELECT statement
    for i in T1Attributes:
        if not commonAttributes.__contains__(i[0]) and not i[0]==Semantics:
            Columns=Columns+i[0]+", "

    #Looping through the Table 2 Attributes to find all the unique columns for the SELECT statement
    for j in T2Attributes:
        if not commonAttributes.__contains__(j[0]) and not j[0]==Semantics:
            Columns=Columns+j[0]+", "

    #print("Select statement : "+Columns) #Columns will be the Attributes for the SELECT statement

    innerJoin=""
    firstExecution=True

    #Looping through the Common attributes to write the INNER JOIN statement
    for i in commonAttributes:
        if firstExecution:
            firstExecution=False
            innerJoin="%s.%s=%s.%s "%(table1,i,table2,i)
        else:
            innerJoin=innerJoin+"AND %s.%s=%s.%s "%(table1,i,table2,i)

    #print("Join statement:"+innerJoin) #innerJoin contains the WHERE ON joining CONDITION

    if Semantics == "StandardSem":
        print("StandardSem")
        q="CREATE TABLE %s SELECT %s %s.StandardSem* %s.StandardSem AS StandardSem FROM %s,%s WHERE %s;"%(TABLENAME,Columns,table1,table2,table1,table2,innerJoin)
        mycursor.execute(q)
        q="DELETE FROM %s WHERE StandardSem=0;"%(TABLENAME)
        mycursor.execute(q)

    elif Semantics == "BagSem":
        print("BagSem")
        q="CREATE TABLE %s SELECT %s %s.BagSem* %s.BagSem AS BagSem FROM %s,%s WHERE %s;"%(TABLENAME,Columns,table1,table2,table1,table2,innerJoin)
        #print(q)
        mycursor.execute(q)

    elif Semantics == "PolynomialSem":
        print("PolynomialSem")
        '''SELECT PRODUCTS_product_id_product_name.product_id, product_name, store_id, CONCAT('(', PRODUCTS_product_id_product_name.PolynomialSem, '*', STOCKS_product_id_store_id.PolynomialSem, ')')
        AS PolynomialSem FROM PRODUCTS_product_id_product_name INNER JOIN STOCKS_product_id_store_id ON PRODUCTS_product_id_product_name.product_id = STOCKS_product_id_store_id.product_id;'''

        q="CREATE TABLE %s SELECT %s CONCAT('(',%s.PolynomialSem,'*',%s.PolynomialSem,')') AS PolynomialSem FROM %s INNER JOIN %s ON %s;"%(TABLENAME,Columns, table1,table2,table1,table2,innerJoin)

        #print(q);
        mycursor.execute(q)
        #print(mycursor.fetchall())

    elif Semantics == "CertaintySem":
        print("CertaintySem")
        q = "CREATE TABLE %s SELECT %s (ROUND(%s.CertaintySem * %s.CertaintySem,2)) AS CertaintySem FROM %s INNER JOIN %s ON %s;" % (TABLENAME, Columns, table1, table2, table1, table2, innerJoin)
        #print(q)
        mycursor.execute(q)

    elif Semantics == "ProbabilitySem":
        print("ProbabilitySem")
        q="CREATE TABLE %s SELECT %s (ROUND(%s.ProbabilitySem * %s.ProbabilitySem,2)) AS ProbabilitySem FROM %s INNER JOIN %s ON %s;"%(TABLENAME,Columns,table1,table2,table1,table2,innerJoin)
        #print(q)
        mycursor.execute(q)

def project(query, Semantics,TABLENAME):
    # #[ColumnName1,ColumnName2,ColumnName3](TableName)
    columns=(query[query.find('[')+1:query.find(']')] )
    table=(query[query.find('(')+1:query.find(')')])

    if Semantics == "StandardSem":
        print("StandardSem")
        q="CREATE TABLE %s SELECT %s , StandardSem FROM %s GROUP BY %s,StandardSem"%(TABLENAME,columns,table,columns)
        #print(q)
        mycursor.execute(q)

    elif Semantics=="BagSem":
        print("BagSem")
        q="CREATE TABLE IF NOT EXISTS %s SELECT %s ,SUM(BagSem) AS BagSem FROM %s GROUP BY %s"%(TABLENAME,columns, table, columns)
        #print(q)
        mycursor.execute(q)

    elif Semantics=="PolynomialSem":
        print("PolynomialSem")
        q = "CREATE TABLE IF NOT EXISTS %s SELECT %s, CONCAT('(',PolynomialSem,')') AS PolynomialSem FROM (SELECT %s, GROUP_CONCAT(PolynomialSem SEPARATOR '+') AS PolynomialSem FROM %s GROUP BY %s) AS T;" %(TABLENAME, columns, columns, table, columns)
        #print(q)
        mycursor.execute(q)

    elif Semantics=="CertaintySem":
        print("CertaintySem")
        q="CREATE TABLE %s SELECT %s,MAX(CertaintySem) AS CertaintySem FROM %s GROUP BY %s "%(TABLENAME,columns,table,columns)
        mycursor.execute(q)

    elif Semantics=="ProbabilitySem":
        #print("ProbabilitySem")
        '''
            #The Algorithm
                #1.Copy all the required columns into a new table
                CREATE TABLE Copy SELECT city,prob FROM TEST;
                
                #2.UPDATE Copy by subtracting 1 with all probabilities
                UPDATE Copy SET prob=1-prob;
                
                #3.Create a LogCopy that will have the log values of all probabilities
                CREATE TABLE LogCopy
                    SELECT city, SUM(LnProb) AS prob FROM(
                        SELECT city, 
                        CASE WHEN prob=0 THEN 4294967295
                        ELSE LN(prob)
                        END AS LnProb FROM Copy
                    ) AS prob GROUP BY city;
                
                #4.UPDATE LogCopy and set every values>1 as 0
                UPDATE LogCopy SET prob=0 WHERE prob>1;
                
                #5.CREATE a final RESULT Table which has the exponent values of the Log values
                CREATE TABLE RESULT 
                    SELECT city, EXP(prob) AS prob FROM LogCopy ;
                
                #6. UPDATE RESULT table by subtracting from 1 execpt if the values are already 1 
                UPDATE RESULT SET prob=1-prob WHERE NOT prob=1;
                
                #7. Print the RESULT table
                SELECT * FROM RESULT;
                
                #8.DROP the Remaining tables
                DROP TABLE Copy;
                DROP TABLE LogCopy;
                DROP TABLE RESULT;
        '''
        #1.
        q="CREATE TABLE IF NOT EXISTS Copy SELECT %s, ProbabilitySem FROM %s;" %(columns,table)
        #print(q)
        mycursor.execute(q)
        #2
        q="UPDATE Copy SET ProbabilitySem=ROUND(1-ProbabilitySem,2);"
        #print(q)
        mycursor.execute(q)
        #3
        q="CREATE TABLE IF NOT EXISTS LogCopy " \
          "SELECT %s,SUM(LnProb) AS ProbabilitySem FROM( SELECT %s, " \
          "CASE WHEN ProbabilitySem=0 THEN 4294967295 ELSE ROUND(LN(ProbabilitySem),2)END AS LnProb FROM Copy )" \
          " AS ProbabilitySem GROUP BY %s;"%(columns,columns,columns)
        #print(q)
        mycursor.execute(q)
        #4
        q="UPDATE LogCopy SET ProbabilitySem=0 WHERE ProbabilitySem>1;"
        #print(q)
        mycursor.execute(q)
        #5
        q="CREATE TABLE IF NOT EXISTS RESULT SELECT %s , ROUND(EXP(ROUND(ProbabilitySem,2)),2) AS ProbabilitySem FROM LogCopy;"%columns
        #print(q)
        mycursor.execute(q)
        #6
        q="UPDATE RESULT SET ProbabilitySem=1-ProbabilitySem WHERE NOT ProbabilitySem=1;"
        #print(q)
        mycursor.execute(q)
        #7
        #q="SELECT %s,ProbabilitySem FROM RESULT;"%columns
        #print(q)
        #mycursor.execute(q)
        #print(mycursor.fetchall())
        #9
        q="DROP TABLE Copy;"
        mycursor.execute(q)
        q="DROP TABLE LogCopy;"
        mycursor.execute(q)
        q="RENAME TABLE RESULT TO "+TABLENAME+";"
        mycursor.execute(q)

        #q="DROP TABLE %s;"%TABLENAME
        # mycursor.execute(q)

def union(query, Semantics,TABLENAME):
    '''
            Algorithm:
            Find all the common columns between the 2 Tables
            UNION ALL them
            CREATE the table with name 'table1_UNION_table2'
            Perform PROJECTION using project('[column1,column2...](table1_UNION_table2)') to remove all the duplicates
    '''

    '''
    
    U[table1](table2)

    '''

    table1=query[query.find('[')+1:query.find(']')]
    table2=query[query.find('(')+1:query.find(')')]

    mycursor.execute("DESCRIBE %s" % table1)
    T1Attributes = mycursor.fetchall()  # Gets all the names of the columns in Table 1
    #print(T1Attributes)
    #mycursor.execute("DESCRIBE %s "% table2)
    #print(mycursor.fetchall())
    Columns=""

    for i in T1Attributes:
        if not i[0]==Semantics:
            Columns=Columns+i[0]+","

    Columns=Columns[:-1]
    #print(Columns)

    if Semantics == "StandardSem":
        print("StandardSem")
        temptable="temp"+TABLENAME
        '''
        CREATE TABLE tempTable3 
                SELECT product_id,StandardSem 
                FROM Table1 
                UNION ALL 
                SELECT product_id,StandardSem
                FROM Table2
                ORDER BY product_id,StandardSem;
                '''

        q="CREATE TABLE %s SELECT %s, StandardSem FROM %s UNION ALL SELECT %s,StandardSem FROM %s ORDER BY %s,StandardSem"%(temptable,Columns,table1,Columns,table2,Columns)
        mycursor.execute(q)

        q="DELETE FROM %s WHERE StandardSem=0"%(temptable)
        mycursor.execute(q)

        q="CREATE TABLE %s SELECT %s,StandardSem FROM %s GROUP BY %s,StandardSem"%(TABLENAME,Columns,temptable,Columns)
        mycursor.execute(q)

        q="DROP TABLE %s"%(temptable)
        mycursor.execute(q)

    elif Semantics == "BagSem":
        print("BagSem")
        '''CREATE TABLE PRODUCTS_product_id_UNION_STOCKS_product_id
        SELECT product_id, SUM(BagSem) AS BagSem
        FROM(SELECT product_id, BagSem FROM PRODUCTS_product_id
        UNION ALL
        SELECT product_id, BagSem FROM STOCKS_product_id
        ORDER BY product_id, BagSem
        ) AS T GROUP BY product_id; '''

        q="CREATE TABLE %s SELECT %s, SUM(BagSem) AS BagSem FROM ( SELECT %s, BagSem FROM %s UNION ALL SELECT %s, BagSem FROM %s ORDER BY %s , BagSem) AS T GROUP BY %s;"%(TABLENAME, Columns,Columns,table1,Columns,table2,Columns,Columns)
        print(q);
        mycursor.execute(q)

    elif Semantics == "PolynomialSem":
        print("PolynomialSem")
        '''
            SELECT product_id,GROUP_CONCAT(PolynomialSem separator'+') FROM(
	            SELECT PRODUCTS_product_id.product_id,PolynomialSem FROM PRODUCTS_product_id
	            UNION ALL
	            SELECT STOCKS_product_id.product_id,PolynomialSem FROM STOCKS_product_id
	            ORDER BY product_id,PolynomialSem
            )AS T
            GROUP BY product_id;
        '''

        q="CREATE TABLE IF NOT EXISTS %s SELECT %s, CONCAT('(',PolynomialSem,')') AS PolynomialSem FROM (SELECT %s , GROUP_CONCAT(PolynomialSem SEPARATOR '+') AS PolynomialSem FROM( SELECT %s, PolynomialSem FROM %s UNION ALL SELECT %s,PolynomialSem FROM %s ORDER BY %s,PolynomialSem)AS T GROUP BY %s) AS T1; "%(TABLENAME,Columns,Columns,Columns,table1,Columns,table2,Columns,Columns)

        print(q)
        mycursor.execute(q)

    elif Semantics == "CertaintySem":
        print("CertaintySem")
        q="CREATE TABLE %s SELECT %s, MAX(CertaintySem) FROM(SELECT %s,CertaintySem FROM %s UNION ALL SELECT %s,CertaintySem FROM %s ORDER BY %s,CertaintySem)AS T GROUP BY %s"%(TABLENAME,Columns,Columns,table1,Columns,table2,Columns,Columns)
        #print(q)
        mycursor.execute(q)

    elif Semantics == "ProbabilitySem":
        print("ProbabilitySem")

        '''Union the 2 tables '''
        q="CREATE TABLE Copy SELECT %s,ProbabilitySem FROM %s UNION ALL SELECT %s,ProbabilitySem FROM %s ORDER BY %s , ProbabilitySem"%(Columns, table1,Columns,table2,Columns)
        mycursor.execute(q)
        ''' Update the Copy table and 1-ProbabilitySem'''
        q="UPDATE Copy SET ProbabilitySem=ROUND(1-ProbabilitySem,2);"
        mycursor.execute(q)

        '''Find the logarithms of the probabilities'''
        q="CREATE TABLE IF NOT EXISTS LogCopy SELECT %s,ROUND(SUM(ROUND(LnProb,2)),2) AS ProbabilitySem FROM(SELECT %s, CASE WHEN ProbabilitySem=0 THEN 4294967295 ELSE LN(ProbabilitySem)END AS LnProb FROM Copy)AS ProbabilitySem GROUP BY %s;"%(Columns,Columns,Columns)
        mycursor.execute(q)

        '''Update LogCopy and SET ProbabilitySem=0 WHERE ProbabiltySem>1'''
        q="UPDATE LogCopy SET ProbabilitySem=0 WHERE ProbabilitySem>1;"
        mycursor.execute(q)

        '''Create the final result table using the exponent values'''
        q="CREATE TABLE IF NOT EXISTS RESULT SELECT %s , ROUND(EXP(ROUND(ProbabilitySem,2)),2) AS ProbabilitySem FROM LogCopy;"%(Columns)
        mycursor.execute(q)

        '''Update the result table and do 1-ProbabilitySem'''
        q="UPDATE RESULT SET ProbabilitySem=ROUND(1-ProbabilitySem ,2 )WHERE NOT ProbabilitySem=1;"
        mycursor.execute(q)

        '''Rename table to TABLENAME'''
        q="RENAME TABLE RESULT TO %s;"%TABLENAME
        mycursor.execute(q)

        '''drop the redundant tables'''
        q="DROP TABLE Copy"
        mycursor.execute(q)
        q="DROP TABLE LogCopy"
        mycursor.execute(q)

def fillDatabase():
    InputSem = input("Select Semantics[0-4] ( 0. Standard ; 1. Bag ; 2. Polynomial ; 3. Probability ; 4. Certainty) : ")
    SelectedSemantics = int(InputSem)
    if SelectedSemantics > 4:
        print("Incorrect Choice:  default selected(0)")
        SelectedSemantics = 0

    mycursor.execute("SHOW DATABASES")
    for db in mycursor:
        if (db == (database,)):
            print(db[0])

    mycursor.execute("SHOW TABLES")

    db = mycursor.fetchall()  # Fetches all the Table Names
    print(db)



    '''If table exists then boolean'''

    Exists = False


    #Checks if the Semantics are already declared in the tables
    for T in db:
        print(T[0] + " -----------------------") #Name of the Table
        mycursor.execute("DESCRIBE %s" % T[0])
        row = mycursor.fetchall()#Attribute
        #print(row)
        for A in row:
            if A[0] == Semantics[SelectedSemantics]: #Attribute name

                Exists = True
                break
        if Exists == True:
            break
        # mycursor.execute("SELECT * FROM %s"%T[0])
        # rows=(mycursor.fetchall())
        '''if(len(rows) > 0):
            print(rows[0])'''

    print(" _________________")
    print(" +++++++++++++++++ ")



    # Adding the semantic Tables
    '''
    for T in db:
                    #table Name     StandardSem         BagSem            PolySem                    ProbabSem              CertainSem
        print("ALTER TABLE %s ADD COLUMN %s INT,  ADD COLUMN %s INT , ADD COLUMN %s VARCHAR(100), ADD COLUMN %s FLOAT, ADD COLUMN %s FLOAT"
                    %(T[0],     Semantics[0] ,     Semantics[1]  ,    Semantics[2] ,          Semantics[3],             Semantics[4])
          )
        AlterTable="ALTER TABLE %s ADD COLUMN %s INT,  ADD COLUMN %s INT , ADD COLUMN %s VARCHAR(100), ADD COLUMN %s FLOAT, ADD COLUMN %s FLOAT" %(T[0],     Semantics[0] ,     Semantics[1]  ,    Semantics[2] ,          Semantics[3],             Semantics[4])
        mycursor.execute(AlterTable)
    '''
    # -----------------------------------------------------------------------------------------------------------------------
    if not Exists:
        annoIndex = 0
        TableNames = ["A", "B", "C", "D","E","F","G","H","I","J"]

        for T in db:
            # table Name     StandardSem         BagSem            PolySem                    ProbabSem              CertainSem
            # print("ALTER TABLE %s ADD COLUMN %s INT,  ADD COLUMN %s INT , ADD COLUMN %s VARCHAR(100), ADD COLUMN %s FLOAT, ADD COLUMN %s FLOAT" %(T[0],     Semantics[SelectedSemantics] ,     Semantics[1]  ,    Semantics[2] ,          Semantics[3],             Semantics[4]))

            print("ADDING " + Semantics[SelectedSemantics] + " Semantics to Table " + T[0])

            if SelectedSemantics == 0 or SelectedSemantics == 1:
                # Standard OR Bag
                AlterTable = "ALTER TABLE %s ADD COLUMN %s INT" % (T[0], Semantics[SelectedSemantics])
                mycursor.execute(AlterTable)

                if SelectedSemantics == 0:  # Standard
                    print("Filling " + Semantics[SelectedSemantics] + " Column of Table " + T[0])
                    # UPDATE products set ProbabilitySem=rand()
                    sqlFormula = "UPDATE " + T[0] + " SET " + Semantics[SelectedSemantics] + "= 1";
                    mycursor.execute(sqlFormula)
                    mycursor.execute("SELECT %s FROM %s" % (Semantics[SelectedSemantics], T[0]))
                    rows = mycursor.fetchall()
                    print(rows)

                elif SelectedSemantics == 1:  # Bag
                    print("Filling " + Semantics[SelectedSemantics] + " Column of Table " + T[0])
                    # UPDATE products SET BagSem =CAST(RAND()*10 AS UNSIGNED);
                    sqlFormula = "UPDATE " + T[0] + " SET " + Semantics[
                        SelectedSemantics] + "= CAST(RAND() * 10 AS UNSIGNED)";
                    mycursor.execute(sqlFormula)
                    mycursor.execute("SELECT %s FROM %s" % (Semantics[SelectedSemantics], T[0]))
                    rows = mycursor.fetchall()
                    print(rows)

                inputDb.commit()


            elif SelectedSemantics == 2:
                # Polynomial
                AlterTable = "ALTER TABLE  %s ADD COLUMN %s VARCHAR(100)" % (T[0], Semantics[SelectedSemantics])
                mycursor.execute(AlterTable)

                print("Filling " + Semantics[SelectedSemantics] + " Column of Table " + T[0])
                mycursor.execute("ALTER TABLE %s ADD ID INT" % (T[0]));  # Add an integer column with numbers
                mycursor.execute("SET @rank=0")
                mycursor.execute("UPDATE %s set ID=@rank:=@rank+1" % (T[0]))

                mycursor.execute("ALTER TABLE %s ADD Anno VARCHAR(10);" % (
                T[0]))  # Add an annotation column that will contain alphabets "A" OR "B" etc
                mycursor.execute("UPDATE %s SET Anno = '%s' " % (T[0], TableNames[annoIndex]))
                annoIndex = annoIndex + 1  # update the annoIndex

                mycursor.execute("UPDATE %s set PolynomialSem=CONCAT(ANNO, ID)" % T[
                    0])  # Concatenate ID and ANNO  and put all its values in PolynomialSem column
                mycursor.execute("ALTER TABLE %s DROP ID,DROP ANNO" % T[0])  # Delete column ID and ANNO

                mycursor.execute("SELECT %s FROM %s" % (Semantics[SelectedSemantics], T[0]))
                rows = mycursor.fetchall()
                print(rows)
                inputDb.commit()

            else:
                # Probability OR Certainity
                AlterTable = "ALTER TABLE  %s ADD COLUMN %s FLOAT" % (T[0], Semantics[SelectedSemantics])
                mycursor.execute(AlterTable)

                print("Filling " + Semantics[SelectedSemantics] + " Column of Table " + T[0])
                # UPDATE products set ProbabilitySem=rand()
                sqlFormula = "UPDATE " + T[0] + " SET " + Semantics[SelectedSemantics] + "= ROUND(rand(),2)";
                mycursor.execute(sqlFormula)
                mycursor.execute("SELECT %s FROM %s" % (Semantics[SelectedSemantics], T[0]))
                rows = mycursor.fetchall()
                print(rows)
                inputDb.commit()

    # -----------------------------------------------------------------------------------------------------------------------

def polynomialProcessing(exp):
    '''
    exp="( ((D1)+D2)*(D1+D3) )"
    result="D1^{2} + D1*D3+ D2*D1 + D2*D3"

    exp="D1^{2} + D1^{2}"
    result=2D1^2
    '''

def Operation(exp,Semantics,TABLENAME):
    #print("Choosing operation ")

    #print(Semantics)
    #print(TABLENAME)

    if exp[1]=='#':
        print("projection Operation")
        project(exp,Semantics,TABLENAME)
    elif exp[1]=='J':
        print("Join Operation")
        join(exp,Semantics,TABLENAME)
    elif exp[1]=='U':
        print("Union Operation")
        union(exp,Semantics,TABLENAME)
    print(exp)

def queryProcessing(query, Semantics):
    '''
        {#[] ( {U { J [{#[]()}]  ({#[]()}) }  ({ J [{#()[]}] ({#()[]}) } } ) }
    '''


    #query=" {#[] (      { U [{ J [{#[]()}]  ({#[]()}) }] ({ J [{#[]()}] ({#[]()}) })  }    ) }"

    #query="{J[{#[product_id](products)}]({#[product_id](stocks)})}"

    query=query.replace(" ","")

    print(query)
    exit=False
    res=1

    while query.__contains__('{'):
        index=0
        forwardBrackIndex = []
        for i in query:
            if query[index]=='{':
                forwardBrackIndex.append(index)
            elif query[index]=='}':
                startBrack=forwardBrackIndex.pop()
                exp=query[startBrack: index+1]
                front=query[0:startBrack]
                back=query[index+1:]
                TABLENAME="Table"+str(res)
                newQ=front+TABLENAME+back
                res=res+1
                query=newQ
                #print(exp) #Send exp to the process based on what the 2nd character is
                Operation(exp,Semantics,TABLENAME)
                #print(q)
                break

            index=index+1

    print("Query Completed ")


queryProcessing("{#[category_id](products)}",Semantics[3])
#select("S[category_id](products)|(product_id>5 )|", Semantics[2],"Table1")

#STANDARD
#select("",Semantics[0])
#project("", Semantics[0])
#join("",Semantics[0])
#union("",Semantics[0])

#BAG
#select("",Semantics[1])
#project("", Semantics[1])
#join("",Semantics[1])
#union("",Semantics[1])

#POLYNOMIAL
#select("",Semantics[2])
#project("", Semantics[2])
#join("",Semantics[2])
#union("",Semantics[2])

#PROBABILITY
#select("",Semantics[3])
#project("", Semantics[3])
#join("",Semantics[3])
#union("",Semantics[3])

#CERTAINTY
#select("",Semantics[4])
#project("", Semantics[4])
#join("",Semantics[4])
#union("",Semantics[4])

mycursor.close()
inputDb.close()