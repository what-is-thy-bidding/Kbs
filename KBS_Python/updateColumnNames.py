import mysql.connector
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

mycursor.execute("SHOW TABLES")

db = mycursor.fetchall()  # Fetches all the Table Names
print(db)


mycursor = inputDb.cursor()
for T in db:
    print(T[0] + " -----------------------")  # Name of the Table
    mycursor.execute("DESCRIBE %s" % T[0])
    row = mycursor.fetchall()  # Attribute
    #print(row)
    for A in row:
        print(T[0]+"_"+A[0] + " "+A[1])   # Attribute name and AttributeType
        newColumnName=""
        if A[1]=='text':
            newColumnName=T[0] + "_" + A[0] + " CHAR(255)"
        else:
            newColumnName = T[0] + "_" + A[0] + " " + A[1]

        Q="ALTER TABLE "+T[0]+" CHANGE "+A[0]+" "+newColumnName
        print(Q)
        mycursor.execute(Q)

mycursor.close()
