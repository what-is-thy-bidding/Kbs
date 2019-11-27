import mysql.connector
import random


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
             "CertaintySem"]  # 4



def join(query, Semantics):
    '''
        The 2 tables to be joined.
        J[table1](table2)
    '''
    query="J[PRODUCTS_product_id_product_name](STOCKS_product_id_store_id)"
    table1=query[query.find('[')+1:query.find(']')]
    table2=query[query.find('(')+1:query.find(')')]

    mycursor.execute("DESCRIBE %s" %table1)
    T1Attributes =mycursor.fetchall()   #Gets all the names of the columns in Table 1
    print(T1Attributes)

    mycursor.execute("DESCRIBE %s" %table2)
    T2Attributes =mycursor.fetchall()   #Gets all the names of the column in Table 2
    print(T2Attributes)

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

    print(Columns) #Columns will be the Attributes for the SELECT statement

    innerJoin=""
    firstExecution=True

    #Looping through the Common attributes to write the INNER JOIN statement
    for i in commonAttributes:
        if firstExecution:
            firstExecution=False
            innerJoin="%s.%s=%s.%s "%(table1,i,table2,i)
        else:
            innerJoin=innerJoin+"AND %s.%s=%s.%s "%(table1,i,table2,i)

    print(innerJoin) #innerJoin contains the WHERE ON joining CONDITION

    if Semantics == "StandardSem":
        print("StandardSem")

    elif Semantics == "BagSem":
        print("BagSem")
        #if we want to save the table
        #TableName="%s_JOIN_%s"(table1,table1)
        #q="CREATE TABLE %s SELECT %s %s.BagSem* %s.BagSem AS BagSem FROM %s,%s WHERE %s;"%(TableName,Columns,table1,table2,table1,table2,innerJoin)

        q="SELECT %s %s.BagSem* %s.BagSem AS BagSem FROM %s,%s WHERE %s;"%(Columns,table1,table2,table1,table2,innerJoin)
        print(q)
        mycursor.execute(q)
        print(mycursor.fetchall())

    elif Semantics == "PolynomialSem":
        print("PolynomialSem")
        '''SELECT PRODUCTS_product_id_product_name.product_id, product_name, store_id, CONCAT('(', PRODUCTS_product_id_product_name.PolynomialSem, '*', STOCKS_product_id_store_id.PolynomialSem, ')')
        AS PolynomialSem FROM PRODUCTS_product_id_product_name INNER JOIN STOCKS_product_id_store_id ON PRODUCTS_product_id_product_name.product_id = STOCKS_product_id_store_id.product_id;'''

        q="SELECT %s CONCAT('(',%s.PolynomialSem,'*',%s.PolynomialSem,')') AS PolynomialSem FROM %s INNER JOIN %s ON %s;"%(Columns, table1,table2,table1,table2,innerJoin)

        print(q);
        #mycursor.execute(q)
        #print(mycursor.fetchall())

    elif Semantics == "CertaintySem":
        print("CertaintySem")

    elif Semantics == "ProbabilitySem":
        print("ProbabilitySem")


def project(query, Semantics):
    print("Project function")
    query="#[product_id,product_name](products)"

    # #[ColumnName1,ColumnName2,ColumnName3](TableName)
    columns=(query[query.find('[')+1:query.find(']')] )
    table=(query[query.find('(')+1:query.find(')')])

    if Semantics == "StandardSem":
        print("StandardSem")

    elif Semantics=="BagSem":
        print("BagSem")
        #This is the original query which helps create a result table
        q="CREATE TABLE IF NOT EXISTS %s SELECT %s ,SUM(BagSem) AS BagSem FROM %s GROUP BY %s"%(table.upper()+"_"+(columns.replace(",","_")),columns, table, columns)
        #q="SELECT %s, SUM(BagSem) AS BagSem FROM %s GROUP BY %s"%(columns,table,columns)
        print(q)
        mycursor.execute(q)
        #print(mycursor.fetchall())

    elif Semantics=="PolynomialSem":
        print("PolynomialSem")
        #This is the original query which helps create a result table
        q = "CREATE TABLE IF NOT EXISTS %s SELECT %s, CONCAT('(',PolynomialSem,')') AS PolynomialSem FROM (SELECT %s, GROUP_CONCAT(PolynomialSem SEPARATOR '+') AS PolynomialSem FROM %s GROUP BY %s) AS T;" %(table.upper() + "_" + (columns.replace(",", "_")), columns, columns, table, columns)
        print(q)

        #SELECT store_id,CONCAT('(',PolynomialSem,')') AS PolynomialSem FROM(SELECT store_id,GROUP_CONCAT(PolynomialSem SEPARATOR'+') AS PolynomialSem FROM stocks GROUP BY store_id) AS T;
        #q="SELECT %s, CONCAT('(',PolynomialSem,')') AS PolynomialSem FROM (SELECT %s, GROUP_CONCAT(PolynomialSem SEPARATOR '+') AS PolynomialSem FROM %s GROUP BY %s) AS T;" %(columns, columns, table, columns)

        mycursor.execute(q)
        #print(mycursor.fetchall())

    elif Semantics=="CertaintySem":
        print("CertaintySem")

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
        q="CREATE TABLE Copy SELECT %s, ProbabilitySem FROM %s;" %(columns,table)
        #print(q)
        mycursor.execute(q)
        #2
        q="UPDATE Copy SET ProbabilitySem=1-ProbabilitySem;"
        #print(q)
        mycursor.execute(q)
        #3
        q="CREATE TABLE LogCopy " \
          "SELECT %s,SUM(LnProb) AS ProbabilitySem FROM( SELECT %s, " \
          "CASE WHEN ProbabilitySem=0 THEN 4294967295 ELSE LN(ProbabilitySem)END AS LnProb FROM Copy )" \
          " AS ProbabilitySem GROUP BY %s;"%(columns,columns,columns)
        #print(q)
        mycursor.execute(q)
        #4
        q="UPDATE LogCopy SET ProbabilitySem=0 WHERE ProbabilitySem>1;"
        #print(q)
        mycursor.execute(q)
        #5
        q="CREATE TABLE RESULT SELECT %s , EXP(ProbabilitySem) AS ProbabilitySem FROM LogCopy;"%columns
        #print(q)
        mycursor.execute(q)
        #6
        q="UPDATE RESULT SET ProbabilitySem=1-ProbabilitySem WHERE NOT ProbabilitySem=1;"
        #print(q)
        mycursor.execute(q)
        #7
        q="SELECT %s,ProbabilitySem FROM RESULT;"%columns
        #print(q)
        mycursor.execute(q)
        #print(mycursor.fetchall())
        #9
        q="DROP TABLE Copy;"
        mycursor.execute(q)
        q="DROP TABLE LogCopy;"
        mycursor.execute(q)
        q="DROP TABLE RESULT;"
        mycursor.execute(q)


def union(query, Semantics):
    '''

    :param query:
    :param Semantics:
    :return:

    U[table1](table2)

    '''
    query="U[products](stocks)"
    table1=query[query.find('[')+1:query.find(']')]
    table2=query[query.find('(')+1:query.find(')')]
    print(table1 + " " + table2)

    if Semantics == "StandardSem":
        print("StandardSem")

    elif Semantics == "BagSem":
        print("BagSem")


    elif Semantics == "PolynomialSem":
        print("PolynomialSem")

    elif Semantics == "CertaintySem":
        print("CertaintySem")

    elif Semantics == "ProbabilitySem":
        print("ProbabilitySem")


def main():
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

    '''
    for T in db:
        print(T[0] + " ===========")
        mycursor.execute("SELECT * FROM  %s "%(T[0]))
        print(mycursor.fetchone())
    '''

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
                sqlFormula = "UPDATE " + T[0] + " SET " + Semantics[SelectedSemantics] + "= rand()";
                mycursor.execute(sqlFormula)
                mycursor.execute("SELECT %s FROM %s" % (Semantics[SelectedSemantics], T[0]))
                rows = mycursor.fetchall()
                print(rows)
                inputDb.commit()

    # -----------------------------------------------------------------------------------------------------------------------

#project("", Semantics[2])
#join("",Semantics[2])
union("",Semantics[2])

mycursor.close()
inputDb.close()