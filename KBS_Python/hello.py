import mysql.connector

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="production"
)
print(mydb)
mycursor=mydb.cursor() # use cursor to communicate with database

#show all the databases in SQL
'''
#mycursor.execute("SHOW DATABASES")
for db in mycursor:
    print(db)
'''

# Create a Table in the database
#mycursor.execute("CREATE TABLE students(name VARCHAR(40),age INT )")

#Print all the Tables in the database
'''mycursor.execute("SHOW TABLES")

for tb in mycursor:
    print(tb)
'''
'''
sqlFormula="INSERT INTO students(name,age) VALUES (%s,%s)" #%s are place holders
student1=("Rachel", 22)
mycursor.execute(sqlFormula,student1)

mydb.commit() #This commit statement save the changes to the database table in MySQL

#instead of just 1 change at a time  we can send an array
students=[("Rachel",12),
            ("Bob",20),
            ("Amanda",22),
            ("Jacob",32)
            ]
mycursor.executemany(sqlFormula,students)
mydb.commit

'''

#How to get all the data from the database
'''
mycursor.execute("SELECT * FROM students")
myresult=mycursor.fetchall() # Fetches all all the rows from the last executed statement
for row in myresult:
    print(row)
'''

'''
#Want a specific Column
mycursor.execute("SELECT age FROM students")
myresult=mycursor.fetchall()
for row in myresult
    print(row)
'''

#getting input from user
'''
name=input("enter your name ")
print("Hello "+name)

'''

#Python will make everything a string unless you specify otherwise
'''
num1=input(Enter number1 : )
num2=input(Enter number2 : )
result= int(num1)+int(num2)
result= float(num1)+float(num2)

'''

#lists
'''
friends=["Kevin","Keren","Jim"]
friends=["Kevin",2,False]
print(friends[0])
print(friends[-1]) #Starts indexing from the BACK of the LIST
print(friends[1:]) #Prints all the items from the index 1
print(friends[1:3]) #Prints from 1 to (3-1) indexs

#List functions

friends.extend(friends) #Add 2 lists together
friends.append("Creed") # Adds to the end of the list
friends.insert(1,"Kelly) # All values are pushed to the right
friends.remove("Jim")
friends.clear()
friends.pop() #get rids of the last element of the list
friends.index("Kevin") # Gets the index of Kevin
friends.count("Jim") #Counts how many jims there are
friends.sort() #Ascending order
friends.reverse()
friends2=friends.copy

'''


#Tuples
'''
coordinates=(4,5)
print(coordinates[0]) #prints 4
'''

#Functions
'''
def say_hi():
    print("Hello User")
    
say_hi()

#--------------------------
#return statement

def cube(num):
    return num*num*num

result=cube(3)
print(result)

#-------------------------
#if statements

is_male=True
is_tall=True

if is_male or/and is_tall:
    print("You are a male")
elif is_male and not(is_tall):
    print("You are not all but a male")
else:
    print("You are a Female")
    
#-----------------------------------

def max_num(num1,num2,num3)
    if num1>=num2 and num1>=num3:
        return num1
    elif num2>=num1 and num2>=num3:
        return num2
    else:
        return num3
    

#------------------------------------
#Dictionary(Key, value ) pair
monthConversions={ 
    "Jan":"January",
    "Fed":"Febuary",
    "Mat":"March"
}

print(montConversions["Mar"])
print(monthConversions.get("Dec", "Not a valid Key"))

'''

#while loops
'''
i=1
while i<=10:
    print(i)
    i=i+1
    i+=1
    
print("Done with loop)

'''

#for loops
'''
for letter in "Akshat":
    print(letter)
    
for index in range(10)
    print(index)
    
for index in range(3,10)
    print(index) #Print all the numbers from 3 to 9
    

for index in range(len(Array))
    print(Array[index])
    

for index in range(5):
    if index==0:
        print("First index")
    else:
        print("Not first index")
'''

#2D lists
'''
number_grid=[
[1,2,3],
[4,5,6],
[7,8,9],
[0]
]

print(number_grid[0][0])

for row in number_grid:
    for col in row:
        print(col)


'''
#importing different python files/modules
'''
import addAnnotation
'''

#Classes and Objects

'''
class Student:
    def __init__(self, Name, Major, gpa, is_on_probation):
        self.Name=Name
        self.Major=Major
        self.gpa=gpa
        self.is_on_probation=is_on_probation
    def on_honour_roll(self):
        if self.gpa>=3.5:
            return true
        else:
            return false
from Student import Student #from Student.py import Student class
student1=Student("Jim","Business",3.1,False)
print(student1.gpa)
'''
