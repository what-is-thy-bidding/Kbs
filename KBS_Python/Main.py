import mysql.connector
import random

# First read the database from the MySQL and add annotation Columns to every Table

# database=input("Database name in mySQL: ")
InputSem = input("Select Semantics[0-4] ( 0. Standard ; 1. Bag ; 2. Polynomial ; 3. Probablility ; 4. Certaininty) : ")

SelectedSemantics = int(InputSem)

if SelectedSemantics > 4:
    print("Incorrect Choice:  default selected(0)")
    SelectedSemantics = 0




database = "production"
inputDb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    database=database
)
print(inputDb)
# Dropping The semantics Tables



mycursor = inputDb.cursor()

mycursor.execute("SHOW DATABASES")
for db in mycursor:
    if (db == (database,)):
        print(db[0])

mycursor.execute("SHOW TABLES")


db = mycursor.fetchall()  # Fetches all the Table Names
print(db)

Semantics = [("StandardSem"),#0
             ("BagSem"),#1
             ("PolynomialSem"),#2
             ("ProbabilitySem"),#3
             "CertainitySem"]#4

'''If table exists then boolean'''

Exists = False

print(" _________________")
print(" +++++++++++++++++ ")



for T in db:
    print(T[0] + " -----------------------") #Name of the Table
    mycursor.execute("DESCRIBE %s" % T[0])
    row = mycursor.fetchall()#Attribute
    print(row)
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
# Adding random floating point values to a column
'''
for T in db:
    print("Filling "+Semantics[SelectedSemantics] +" Column of Table "+ T[0])
    #UPDATE products set ProbabilitySem=rand()
    sqlFormula="UPDATE "+ T[0] +" SET "+ Semantics[SelectedSemantics] +"= rand()";
    print(sqlFormula)
    mycursor.execute(sqlFormula)
    mycursor.execute("SELECT %s FROM %s" %(Semantics[SelectedSemantics], T[0]))
    rows = mycursor.fetchall()
    print(rows)
    inputDb.commit()
'''

# -----------------------------------------------------------------------------------------------------------------------
DropSemantics=int(input("Input the semantics to drop (if not then -1) : "))
if DropSemantics>=0:
    for T in db:
        mycursor.execute("ALTER TABLE %s DROP %s"%(T[0], Semantics[DropSemantics]))
        #mycursor.execute("ALTER TABLE %s DROP %s"%(T[0],Semantics[0]))
        #mycursor.execute("ALTER TABLE %s DROP %s"%(T[0],Semantics[1]))
        #mycursor.execute("ALTER TABLE %s DROP %s"%(T[0],Semantics[2]))
        #mycursor.execute("ALTER TABLE %s DROP %s"%(T[0],Semantics[3]))
        #mycursor.execute("ALTER TABLE %s DROP %s"%(T[0],Semantics[4]))









'''
QueryAnswerDb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
)
print(QueryAnswerDb)
# Dropping The semantics Tables
QueryAnswerCursor = QueryAnswerDb.cursor()
QueryAnswerCursor.execute("CREATE DATABASE IF NOT EXISTS QueryResults")
'''



Query=""
queryNumber=0
while not (Query == "exit"):
    Query=input("Enter Query (to end query type ['exit']) : ")

    if not Query == "exit":
        queryNumber=queryNumber+1
        if "UNION" in Query:
            # '+'
            print("This is a union query ")

            #Table 1
            SELECT1 = input("Input Table 1 SELECT Parameters  :")
            FROM1 = input("Input Table 1 FROM Parameters :")
            WHERE1 = input("Input Table 1 WHERE Condition : ")

            #Table 2
            SELECT2 = input("Input Table 2 SELECT Parameters  :")
            FROM2 = input("Input Table 2 FROM Parameters :")
            WHERE2 = input("Input Table 2 WHERE Condition : ")


            if SelectedSemantics==0:#Standard Semantics
                print("Standard Semantics")
            elif SelectedSemantics==1:#Bag Semantics
                Q1 = "SELECT " + SELECT1 + " ,SUM(BagSem) as BagSem FROM (SELECT DISTINCT " + SELECT1 + " , " + FROM1 + "." + \
                     Semantics[SelectedSemantics] + "*" + FROM1 + "." + Semantics[
                         SelectedSemantics] + " AS BagSem FROM " + FROM1 + " WHERE " + WHERE1 + ")AS T1 GROUP BY (" + SELECT1 + ")"

                Q2 = "SELECT " + SELECT2 + " ,SUM(BagSem) as BagSem FROM (SELECT DISTINCT " + SELECT2 + " , " + FROM2 + "." + \
                     Semantics[SelectedSemantics] + "*" + FROM2 + "." + Semantics[
                         SelectedSemantics] + " AS BagSem FROM " + FROM2 + " WHERE " + WHERE2 + ")AS T2 GROUP BY (" + SELECT2 + ")"

                unionQ = "SELECT " + SELECT1 + " ,SUM(BagSem) FROM (" + Q1 + "union all " + Q2 + ")AS T GROUP BY (" + SELECT1 + ");"
                print(unionQ)
                mycursor.execute(unionQ)
                print(mycursor.fetchall())
                print("Bag Semantics")

            elif SelectedSemantics==2:#Polynomial Semantics
                print("Polynomial Semantics")
                '''Q1 = "SELECT " + SELECT1 + " ,group_concat(jinann separator '+' ) as jinann FROM (SELECT DISTINCT " + SELECT1 + " ,concat('(', " + FROM1 + "." + \
                     Semantics[SelectedSemantics] + ",'*'," + FROM1 + "." + Semantics[
                         SelectedSemantics] + " ,')') as jinann FROM " + FROM1 + " WHERE " + WHERE1 + ")AS T1 GROUP BY (" + SELECT1 + ")"

                Q2 = "SELECT " + SELECT2 + " ,group_concat(jinann separator '+' ) as jinann FROM (SELECT DISTINCT " + SELECT2 + " ,concat('(', " + FROM2 + "." + \
                     Semantics[SelectedSemantics] + ",'*'," + FROM2 + "." + Semantics[
                         SelectedSemantics] + " ,')') as jinann FROM " + FROM2 + " WHERE " + WHERE2 + ")AS T1 GROUP BY (" + SELECT2 + ")"

                unionQ="SELECT " + SELECT1 + " ,group_concat(jinann separator '+' ) as polynomial FROM (" + Q1 + "union all " + Q2 + ")AS T GROUP BY (" + SELECT1 + ");"
                
                print(unionQ)
                mycursor.execute(unionQ)
                print(mycursor.fetchall())
                '''
            elif SelectedSemantics==3:#Probability Semantics
                print("Probability Semantics")

            elif SelectedSemantics==4:#Certainty Semantics
                print("Certainty Semantics")
            else:
                break


        elif "JOIN" in Query:

            print("This is a join query ")
            SELECT = input("Input SELECT Parameters  :") #products_product_id, products_product_name
            FROM   = input("Input FROM Parameters :") #products,stocks
            WHERE  = input("Input WHERE Condition : ") #products_product_id=stocks_product_id
            Tnames = FROM.split(",")

            '''print(SELECT)
            print(FROM)
            print(WHERE)'''

            '''joinCondition=""

            for i in WHERE:
                if (i.__contains__("=") and i.count(".") == 2) and (not i.__contains__("!")) and (not i.__contains__("<")) and (not i.__contains__(">")):
                    joinCondition = i
                    break
            '''

            # '*'
            if SelectedSemantics == 0:  # Standard Semantics
                print("Standard Semantics")
            elif SelectedSemantics == 1:  # Bag Semantics
                print("Bag Semantics")
                Q="SELECT "+SELECT+" ,SUM(BagSem) FROM (SELECT DISTINCT "+SELECT + " , "+Tnames[0]+"."+Semantics[SelectedSemantics] + "*"+Tnames[1]+"."+Semantics[SelectedSemantics] + " AS BagSem FROM "+FROM + " WHERE "+WHERE + ")AS T GROUP BY "+SELECT
                print(Q)
                mycursor.execute(Q)
                print(mycursor.fetchall())

            elif SelectedSemantics == 2:  # Polynomial Semantics
                print("Polynomial Semantics")

            elif SelectedSemantics == 3:  # Probability Semantics
                print("Probability Semantics")
            elif SelectedSemantics == 4:  # Certainty Semantics
                print("Certainty Semantics")

            else:
                break


        else:
            print("Normal Query")
            if SelectedSemantics == 0:  # Standard Semantics
                print("Standard Semantics")
            elif SelectedSemantics == 1:  # Bag Semantics
                print("Bag Semantics")
            elif SelectedSemantics == 2:  # Polynomial Semantics
                print("Polynomial Semantics")
            elif SelectedSemantics == 3:  # Probability Semantics
                print("Probability Semantics")
            elif SelectedSemantics == 4:  # Certainty Semantics
                print("Certainty Semantics")
            else:
                break

    elif Query=="exit":
        break







































mycursor.close()
inputDb.close()