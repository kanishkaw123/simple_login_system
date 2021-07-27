
from mysql.connector import MySQLConnection
import mysql.connector
Connection=mysql.connector.connect(host='127.0.0.1',user='root',password='kanishka12@AB',database='user_data')
cursor=Connection.cursor()

#the class used to store properies of instances.
class user:
    def __init__(self):
        self.id=None
        self.name=None
        self.surname=None
        self.email=None
        self.username=None
        self.password=None
        
client=user()

#checking whether the user is registered
def exisiting_customer():
    username=input("please enter your username: \n")
    password=input("please enter your password: \n")
    qurey=("SELECT user_id , firstname, surname, email FROM users WHERE username=%s AND password=%s")
    cursor.execute(qurey,(username, password,))
    for i in cursor:
        client.id=i[0]
        client.name=i[1]
        client.surname=i[2]
        client.email=i[3]
    print(client.name,client.surname,client.email,client.username,client.password)
#creating a new account
def create_new():
    #getting email and validating it
    def getEmail():
        clEmail=input("Please enter your email address: \n")
        atCheck=0
        for char in clEmail:
            if char=="@":
                atCheck+=1
            else:
                pass
        if atCheck!=1:
            print("Please enter a valid email addess")
            getEmail()
        else:
            exEmail=("SELECT email FROM users")
            cursor.execute(exEmail)
            exEmails=[]
            for item in cursor:
                for email in item:
                    exEmails.append(email)
            if clEmail in exEmails:
                print("You already have an account with us!")
                decision=input("Do you want to register with another email(y/n)? \n")
                if decision==("y"):
                    getEmail()
                else:
                    customer_status_checker()
            else:
                getUsername(clEmail)
    #getting username
    def getUsername(clEmail):
        username=input("please enter your username: \n").strip()
        usernames=[]
        qurey=("SELECT username from users")
        cursor.execute(qurey)
        for i in cursor:
            for item in i:
                usernames.append(item)
        if username in usernames:
            print("Sorry! That username is not available.")
            getUsername(clEmail)
        else:
            getPassword(username,clEmail)


    #getting password and validating it
    def getPassword(username,clEmail):
        password=input("please enter your password: \n")
        
        symbols=["@","£","&"]
        spChar=["!",",","^","*","-","+"]
        capCount=0
        spCharCount=0
        numberCount=0

        
        for letter in password:
            if letter.isupper():
                capCount+=1
            elif letter in spChar:
                spCharCount+=1
            elif letter.isnumeric():
                numberCount+=1
            else:
                pass
    
        if capCount<1:
            print("You must include at least one capital letter in your password." )
            getPassword(username,clEmail)

        elif spCharCount>0:
            print("You cannot use {} in your password".format(spChar))
            getPassword(username,clEmail)

        elif numberCount<=1:
            print("You must include atleast one number in your password")  
            getPassword(username,clEmail)

        else:
            fetchDataToDatabase(username,password,clEmail)

    #insering data to the database
    def fetchDataToDatabase(username,password,clEmail):
        clFirstName=input("Please enter your first name: \n")
        clSurName=input("Please enter your surname: \n")
        client.name=clFirstName
        client.surname=clSurName
        client.email=clEmail
        client.username=username
        client.password=password
        authentication()

    #authenticating data
    def authentication():
        print("DATA YOU ENTERED: \n USERNAME: {} \n FIRST NAME: {}\n SURNAME: {} \n E-MAIL: {}".format(client.username,client.name,client.surname,client.email))
        authority=input("Do you want to continue? (y/n) \n")
        if authority=="y":
            qurey=("INSERT INTO users (firstname,surname,email,username,password) VALUES (%s,%s,%s,%s,%s)")
            data=(client.name,client.surname,client.email,client.username,client.password)
            cursor.execute(qurey,data)
            Connection.commit()
        userID=("SELECT user_id FROM users WHERE username=%s AND password=%s")
        cursor.execute(userID,(client.username,client.password,))
        for user_ID in cursor:
            for i in user_ID:
                print("your user ID is: {}".format(i))
        customer_status_checker()
    
    getEmail()


#checking if user registered.
def customer_status_checker():
    status=input("Do you have an existing account? \n")
    if "y"==status or "yes"==status:
        exisiting_customer()
    else:
        create_new()


#running the starter function
if __name__=="__main__":
    customer_status_checker()

