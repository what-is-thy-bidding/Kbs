import mysql.connector
import random
# First read the database from the MySQL and add annotation Columns to every Table

#database=input("Database name in mySQL: ")
InputSem=input("Select Semantics[0-4] ( 0. Standard ; 1. Bag ; 2. Polynomial ; 3. Probablility ; 4. Certaininty) : ")

SelectedSemantics=int(InputSem)

if SelectedSemantics>4:
    print("Incorrect Choice:  default selected(0)")
    SelectedSemantics=0

database="production"
inputDb=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    database=database
)
print(inputDb)

mycursor=inputDb.cursor()


mycursor.execute("SHOW DATABASES")
for db in mycursor:
    if(db==(database,)):
        print(db[0])


mycursor.execute("SHOW TABLES")

db=mycursor.fetchall() # Fetches all the Table Names
print(db)

print(" _________________")
print(" +++++++++++++++++ ")

for T in db:
    print(T[0] + " -----------------------")
    mycursor.execute("DESCRIBE %s" %T[0])
    print(mycursor.fetchall())
    mycursor.execute("SELECT * FROM %s"%T[0])
    rows=(mycursor.fetchall())
    if(len(rows) > 0):
        print(rows[0])



'''
for T in db:
    print(T[0] + " ===========")
    mycursor.execute("SELECT * FROM  %s "%(T[0]))
    print(mycursor.fetchone())
'''

print(" _________________")
print(" +++++++++++++++++ ")


Semantics=[("StandardSem"),
           ("BagSem"),
           ("PolynomialSem"),
           ("ProbabilitySem"),
           "CertainitySem"]


# Dropping The semantic Tables
'''
for T in db:
    mycursor.execute("ALTER TABLE %s DROP %s"%(T[0], Semantics[SelectedSemantics]))
    
    #mycursor.execute("ALTER TABLE %s DROP %s"%(T[0],Semantics[0]))
    #mycursor.execute("ALTER TABLE %s DROP %s"%(T[0],Semantics[1]))
    #mycursor.execute("ALTER TABLE %s DROP %s"%(T[0],Semantics[2]))
    #mycursor.execute("ALTER TABLE %s DROP %s"%(T[0],Semantics[3]))
    #mycursor.execute("ALTER TABLE %s DROP %s"%(T[0],Semantics[4]))
'''



#Adding the semantic Tables
'''
for T in db:
                #table Name     StandardSem         BagSem            PolySem                    ProbabSem              CertainSem
    print("ALTER TABLE %s ADD COLUMN %s INT,  ADD COLUMN %s INT , ADD COLUMN %s VARCHAR(100), ADD COLUMN %s FLOAT, ADD COLUMN %s FLOAT"
                %(T[0],     Semantics[0] ,     Semantics[1]  ,    Semantics[2] ,          Semantics[3],             Semantics[4])
      )
    AlterTable="ALTER TABLE %s ADD COLUMN %s INT,  ADD COLUMN %s INT , ADD COLUMN %s VARCHAR(100), ADD COLUMN %s FLOAT, ADD COLUMN %s FLOAT" %(T[0],     Semantics[0] ,     Semantics[1]  ,    Semantics[2] ,          Semantics[3],             Semantics[4])
    mycursor.execute(AlterTable)
'''

for T in db:
                #table Name     StandardSem         BagSem            PolySem                    ProbabSem              CertainSem
    #print("ALTER TABLE %s ADD COLUMN %s INT,  ADD COLUMN %s INT , ADD COLUMN %s VARCHAR(100), ADD COLUMN %s FLOAT, ADD COLUMN %s FLOAT" %(T[0],     Semantics[SelectedSemantics] ,     Semantics[1]  ,    Semantics[2] ,          Semantics[3],             Semantics[4]))

    print("ADDING " + Semantics[SelectedSemantics] + " Semantics to Table "+T[0])

    if SelectedSemantics==0 or SelectedSemantics==1:
        #Standard OR Bag
        AlterTable = "ALTER TABLE %s ADD COLUMN %s INT" % (T[0], Semantics[SelectedSemantics])
        mycursor.execute(AlterTable)

        if SelectedSemantics==0: #Standard
            print("Filling " + Semantics[SelectedSemantics] + " Column of Table " + T[0])
            # UPDATE products set ProbabilitySem=rand()
            sqlFormula = "UPDATE " + T[0] + " SET " + Semantics[SelectedSemantics] + "= 1";
            mycursor.execute(sqlFormula)
            mycursor.execute("SELECT %s FROM %s" % (Semantics[SelectedSemantics], T[0]))
            rows = mycursor.fetchall()
            print(rows)

        elif SelectedSemantics==1: #Bag
            print("Filling " + Semantics[SelectedSemantics] + " Column of Table " + T[0])
            # UPDATE products SET BagSem =CAST(RAND()*10 AS UNSIGNED);
            sqlFormula = "UPDATE " + T[0] + " SET " + Semantics[SelectedSemantics] + "= CAST(RAND() * 10 AS UNSIGNED)";
            mycursor.execute(sqlFormula)
            mycursor.execute("SELECT %s FROM %s" % (Semantics[SelectedSemantics], T[0]))
            rows = mycursor.fetchall()
            print(rows)

        inputDb.commit()


    elif SelectedSemantics==2:
        #Polynomial
        AlterTable="ALTER TABLE  %s ADD COLUMN %s VARCHAR(100)"%(T[0], Semantics[SelectedSemantics])
        mycursor.execute(AlterTable)

    else:
        #Probability OR Certainity
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


#Adding random floating point values to a column
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