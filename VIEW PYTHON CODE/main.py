from mysql.connector import MySQLConnection
import mysql.connector
from tkinter import *
import os
import sys
#tkinter and mysql modules are already imported when importing clientClass
#configuring the main window

class user:
        def __init__(self):
            self.id=""
            self.firstname=""
            self.surname=""
            self.email=""
            self.data=""
            self.username=""
            self.password=""
            self.exUser=False

        def getEmail(self,clEmail,exEmails):
            
            invalidEmail=False
            #validating email
            if "@" in clEmail:
                email=clEmail.split("@")
                if len(email)>2:
                    invalidEmail=True
                if "." not in email[1]:
                    invalidEmail=True
                for part in email:
                    for char in part:
                        if (char=="." and part.index(char)==0) or (char=="." and part[part.index(char)+1]==".") or (char=="." and part.index(char)==(len(part)-1)):
                            invalidEmail=True
                    if " " in part:
                        invalidEmail=True
            else:
                invalidEmail=True

            if invalidEmail:
                return "invalidEmail"
            else:
                if clEmail in exEmails:
                    return "existingEmail"
                else:
                    self.email=clEmail
        
        def getUsername(self,username,usernames):
            if len(username)>20:
                return "longUsername"
    
            if username in usernames:
                return "unavailableUsername"
            else:
                self.username=username

        def getPassword(self,password):

            if password==self.username:
                return "usernamePassword"
            else:
                symbols=["@","£","&"]
                spChar=["!",",","^","*","-","+"]
                capCount=0
                capC=False
                spCharCount=0
                spC=False
                numberCount=0
                numC=False
                symbolCount=0
                symC=False
                getPasswordAgain=False

                #checking passwords for a specific criteriea 
                for letter in password:
                    if letter.isupper():
                        capCount+=1
                    elif letter in symbols:
                        symbolCount+=1
                    elif letter in spChar:
                        spCharCount+=1
                    elif letter.isnumeric():
                        numberCount+=1
                    else:
                        pass
            
                if capCount<1:
                    print("You must include at least one capital letter in your password." )
                    getPasswordAgain=True
                    capC=True

                if spCharCount>0:
                    print("You cannot use {} in your password".format(spChar))
                    getPasswordAgain=True
                    spC=True

                if numberCount<=1:
                    print("You must include atleast one number in your password")  
                    getPasswordAgain=True
                    numC=True
                
                if symbolCount==0:
                    print(f"You must include atleast one from {symbols} in your password")  
                    getPasswordAgain=True
                    symC=True

                if getPasswordAgain:
                    return "invalidPassword"
                else:
                    self.password=password

        def getNames(self,firstName,lastName):
                if len(firstName)<3 or len(lastName)<3:
                    return False
                else:
                    self.name=firstName+lastName

        def getData(self,data):
            self.data=data

def main():
    root = Tk()
    root.geometry("1000x800")
    root.configure(bg='#9B9696')

    thisFolder=os.path.dirname(os.path.abspath(__file__))
    connFile=os.path.join(getattr(sys, '_MEIPASS', thisFolder) ,"conn.data")

    connDataFile= open(connFile,"r")
    connData=connDataFile.read().split()
    connDataFile.close()

    thisFolder=os.path.dirname(os.path.abspath(__file__))
    baseFile=os.path.join(getattr(sys, '_MEIPASS', thisFolder),"database.name")

    baseDataFile= open(baseFile,"r")
    baseData=baseDataFile.read().split()
    baseDataFile.close()
    
    Connection=""
    cursor=""

    try:
        Connection=mysql.connector.connect(host=connData[0],user=connData[1],password=connData[2],database=baseData[0],auth_plugin="mysql_native_password")
        cursor=Connection.cursor(buffered=True)
    except:
        Connection=mysql.connector.connect(host=connData[0],user=connData[1],password=connData[2],auth_plugin="mysql_native_password")
        cursor=Connection.cursor(buffered=True)
        
        cursor.execute("CREATE DATABASE user_data")
        cursor.execute('''CREATE TABLE users ( user_id int not null primary key auto_increment, 
                        firstname varchar(30) not null, 
                        surname varchar(40) not null, 
                        email varchar(70) not null,
                        username varchar(20) not null,
                        password varchar(16) not null,
                        data text null)''')
        cursor.execute("alter table users auto_increment=1000")

        baseData=open(baseFile,"w")
        baseData.write("user_data")
        baseData.close()


    #the class used to store properies of instances.

    def updateSubmit(existingUserObject,frame):
        try:
            qurey=("UPDATE users SET firstname=%s,surname=%s,data=%s WHERE username=%s")
            data=(existingUserObject.firstname,existingUserObject.surname,existingUserObject.data,existingUserObject.username)
            cursor.execute(qurey,data)
            Connection.commit()
            lastLabel=Label(frame, text="Update Success", width=50, font="Verdana 9 bold",fg="red")
            lastLabel.grid(row=8, column=0, columnspan=2)
        except:
            lastLabel=Label(frame, text="Update Failed", width=50, font="Verdana 9 bold",fg="red")
            lastLabel.grid(row=8, column=0, columnspan=2)

    def update(existingUserUpdate,loggedFrame):
        loggedFrame.destroy()
        updateUserFrame = Frame(root, width=50)
        updateUserFrame.pack(fill="both", expand=True)
        updateUserFrame.place(in_=root, anchor="c", relx=.5, rely=.5)

        title = Label(updateUserFrame, text="Enter your other data", width=50,pady=10, font="Verdana 13 bold",background="#5F5F5F",fg="white")
        title.grid(row=0, column=0, columnspan=2)

        gapLabel=Label(updateUserFrame, text="", width=50, font="Verdana 10 bold")
        gapLabel.grid(row=1, column=0, columnspan=2)

        fNameLabel = Label(updateUserFrame, text="First Name", width=15,font="Verdana 10 bold")
        fNameLabel.grid(row=2,column=0)

        fName=StringVar()
        fName.set(existingUserUpdate.firstname)
        fNameEntry = Entry(updateUserFrame, textvariable=fName, width=35,font="Verdana 10")
        fNameEntry.grid(row=2, column=1) 
        
        lNameLabel = Label(updateUserFrame, text="Last Name", width=15,font="Verdana 10 bold")
        lNameLabel.grid(row=3,column=0)


        lName=StringVar()
        lName.set(existingUserUpdate.surname)
        lNameEntry = Entry(updateUserFrame, textvariable=lName, width=35,font="Verdana 10")
        lNameEntry.grid(row=3, column=1) 

        emailLabel = Label(updateUserFrame, text="E-Mail", width=15,font="Verdana 10 bold")
        emailLabel.grid(row=4,column=0)

        email=StringVar()
        email.set(existingUserUpdate.email)
        emailLabel = Entry(updateUserFrame, textvariable=email, width=35,font="Verdana 10")
        emailLabel.grid(row=4,column=1)

        dataLabel = Label(updateUserFrame, text="Data", width=15,font="Verdana 10 bold")
        dataLabel.grid(row=5,column=0)

        otherData=StringVar()
        otherData.set(existingUserUpdate.data)
        otherDataEntry = Entry(updateUserFrame, textvariable=otherData, width=35,font="Verdana 10")
        otherDataEntry.grid(row=5,column=1)

        lastBeforeLabel=Label(updateUserFrame, text="", width=50, font="Verdana 10 bold")
        lastBeforeLabel.grid(row=6, column=0, columnspan=2) 

        ExitButton = Button(updateUserFrame, text="Exit", width=20,command=lambda: exit())
        ExitButton.grid(row=7, column=0)

        nextButton = Button(updateUserFrame, text="Update", width=20,command=lambda: updateSubmit(existingUserUpdate,updateUserFrame))
        nextButton.grid(row=7, column=1)

        lastLabel=Label(updateUserFrame, text="", width=50, font="Verdana 10 bold")
        lastLabel.grid(row=8, column=0, columnspan=2)

    def login(inputPassword, inputUsername, secondFrame):

        existingUserObject = user()
        existingUserObject.username = inputUsername.get().strip()
        existingUserObject.password = inputPassword.get().strip()
        qurey = ("SELECT user_id , firstname, surname, email, data FROM users WHERE username=%s AND password=%s")
        cursor.execute(qurey, (existingUserObject.username, existingUserObject.password,))
        if cursor.rowcount >= 1:
            for i in cursor:
                existingUserObject.id = i[0]
                existingUserObject.firstname = i[1]
                existingUserObject.surname = i[2]
                existingUserObject.email = i[3]
                existingUserObject.data = i[4]

            secondFrame.destroy()
            loggedFrame = Frame(root, width=400, height=250)
            loggedFrame.pack(fill="both", expand=True)
            loggedFrame.place(in_=root, anchor="c", relx=.5, rely=.5)

            title = Label(loggedFrame, text="Your Data", width=60, font="Verdana 13 bold",background="#5F5F5F",fg="white")
            title.grid(row=0, column=0, columnspan=2)

            idLabel = Label(loggedFrame, text="ID", width=25,font="Verdana 10 bold")
            idLabel.grid(row=1,column=0)

            idDataLabel = Label(loggedFrame, text=existingUserObject.id, width=35,font="Verdana 10")
            idDataLabel.grid(row=1,column=1)

            nameLabel = Label(loggedFrame, text="Name", width=25,font="Verdana 10 bold")
            nameLabel.grid(row=2,column=0)

            nameDataLabel = Label(loggedFrame, text=existingUserObject.firstname + existingUserObject.surname, width=35,font="Verdana 10")
            nameDataLabel.grid(row=2,column=1)

            emailLabel = Label(loggedFrame, text="E-Mail", width=25,font="Verdana 10 bold")
            emailLabel.grid(row=3,column=0)

            emailDataLabel = Label(loggedFrame, text=existingUserObject.email, width=35,font="Verdana 10")
            emailDataLabel.grid(row=3,column=1)

            dataLabel = Label(loggedFrame, text="Data", width=25,font="Verdana 10 bold")
            dataLabel.grid(row=4,column=0)

            dataDataLabel = Label(loggedFrame, text=existingUserObject.data, width=35,font="Verdana 10")
            dataDataLabel.grid(row=4,column=1)

            lastBeforeLabel=Label(loggedFrame, text="", width=50, font="Verdana 10 bold")
            lastBeforeLabel.grid(row=5, column=0, columnspan=2) 

            ExitButton = Button(loggedFrame, text="Exit", width=20,command=lambda: exit())
            ExitButton.grid(row=6, column=0)

            updateButton = Button(loggedFrame, text="Update", width=20,command=lambda: update(existingUserObject,loggedFrame))
            updateButton.grid(row=6, column=1)

            lastLabel=Label(loggedFrame, text="", width=50, font="Verdana 10 bold")
            lastLabel.grid(row=7, column=0, columnspan=2) 

        elif cursor.rowcount == 0:
            label3 = Label(secondFrame, text="No records detected", width=40, fg="red")
            label3.grid(row=4, column=0, columnspan=2)


    def exitingUser(currentFrame):
        # creating frame for the login
        currentFrame.destroy()

        secondFrame = Frame(root, width=500, height=250)
        secondFrame.pack(fill="both", expand=True)
        secondFrame.place(in_=root, anchor="c", relx=.5, rely=.5)

        heading = Label(secondFrame, text="Enter your login details", width=60, font="Verdana 11 bold", pady=10, fg="white", background="#5F5F5F")
        heading.grid(row=0, column=0, columnspan=2)
        label7 = Label(secondFrame, text="", width=20)
        label7.grid(row=1, column=1)
        label1 = Label(secondFrame, text="Please enter your username:", width=25, font="Verdana 10")
        label1.grid(row=2, column=0)
        label2 = Label(secondFrame, text="Please enter your password:", width=25, font="Verdana 10")
        label2.grid(row=3, column=0)

        inputUsername = Entry(secondFrame, width=35)
        inputUsername.grid(row=2, column=1)

        inputPassword = Entry(secondFrame, width=35)
        inputPassword.grid(row=3, column=1)

        label4 = Label(secondFrame, text="", width=20)
        label4.grid(row=4, column=1)

        loginButton = Button(secondFrame, text="Login", width=20,command=lambda: login(inputPassword, inputUsername,secondFrame))
        loginButton.grid(row=5, column=1)

        def goBack():
            secondFrame.destroy()
            User_status_checker()

        nextButton = Button(secondFrame, text="Back", width=20, command=goBack)
        nextButton.grid(row=5, column=0)

        label6 = Label(secondFrame, text="", width=20)
        label6.grid(row=6, column=1)

    def submitNewData(newUser,fNameEntry,lNameEntry,otherDataEntry, newUserFrame4 ):
        newUser.firstname=fNameEntry.get()
        newUser.lastname=lNameEntry.get()
        newUser.data=otherDataEntry.get()
        if len(newUser.firstname)<3 or len(newUser.lastname)<3:
            lastLabel=Label(newUserFrame4, text="Your names cannot be smaller than 3 characters", width=50, font="Verdana 9", fg="red")
            lastLabel.grid(row=8, column=0, columnspan=2)
        else:
            qurey=("INSERT INTO users (firstname,surname,email,username,password,data) VALUES (%s,%s,%s,%s,%s,%s)")
            data=(newUser.firstname,newUser.surname,newUser.email,newUser.username,newUser.password,newUser.data)
            cursor.execute(qurey,data)
            Connection.commit()
            userID=("SELECT user_id FROM users WHERE username=%s AND password=%s")
            cursor.execute(userID,(newUser.username,newUser.password,))
            for user_ID in cursor:
                for i in user_ID:
                    newUserFrame4.destroy()
                    newUserFrame5=Frame(root, width=100, height=250)
                    newUserFrame5.pack(fill="both", expand=True, padx=20, pady=20)
                    newUserFrame5.place(in_=root, anchor="c", relx=.5, rely=.5)

                    label1 = Label(newUserFrame5, text="Your id is {}".format(i), width=80, pady=20, font="Verdana 10 bold")
                    label1.grid(row=0, column=0, columnspan=2)

                    loginButton = Button(newUserFrame5, text="Exit", width=20, command=lambda: exit())
                    loginButton.grid(row=2, column=0)

                    loginButton = Button(newUserFrame5, text="Login", width=20, command=lambda: exitingUser(newUserFrame5))
                    loginButton.grid(row=2, column=1)

                    lastLabel=Label(newUserFrame5, text="", width=80, pady=20, font="Verdana 10 bold")
                    lastLabel.grid(row=3, column=0, columnspan=2)

    def newOtherData(newUser):

        newUserFrame4 = Frame(root, width=50)
        newUserFrame4.pack(fill="both", expand=True)
        newUserFrame4.place(in_=root, anchor="c", relx=.5, rely=.5)

        title = Label(newUserFrame4, text="Enter your other data", width=50,pady=10, font="Verdana 13 bold",background="#5F5F5F",fg="white")
        title.grid(row=0, column=0, columnspan=2)

        gapLabel=Label(newUserFrame4, text="", width=50, font="Verdana 10 bold")
        gapLabel.grid(row=1, column=0, columnspan=2)

        fNameLabel = Label(newUserFrame4, text="First Name", width=15,font="Verdana 10 bold")
        fNameLabel.grid(row=2,column=0)

        fNameEntry = Entry(newUserFrame4,width=35)
        fNameEntry.grid(row=2, column=1) 

        lNameLabel = Label(newUserFrame4, text="Last Name", width=15,font="Verdana 10 bold")
        lNameLabel.grid(row=3,column=0)

        lNameEntry = Entry(newUserFrame4,width=35)
        lNameEntry.grid(row=3, column=1) 

        emailLabel = Label(newUserFrame4, text="E-Mail", width=15,font="Verdana 10 bold")
        emailLabel.grid(row=4,column=0)

        emailLabel = Label(newUserFrame4, text=newUser.email, width=35,font="Verdana 10 bold")
        emailLabel.grid(row=4,column=1)

        dataLabel = Label(newUserFrame4, text="Data", width=15,font="Verdana 10 bold")
        dataLabel.grid(row=5,column=0)

        otherDataEntry = Entry(newUserFrame4,width=35)
        otherDataEntry.grid(row=5,column=1)

        lastBeforeLabel=Label(newUserFrame4, text="", width=50, font="Verdana 10 bold")
        lastBeforeLabel.grid(row=6, column=0, columnspan=2) 

        nextButton = Button(newUserFrame4, text="Submit", width=20,command=lambda: submitNewData(newUser,fNameEntry,lNameEntry,otherDataEntry,newUserFrame4))
        nextButton.grid(row=7, column=1)

        lastLabel=Label(newUserFrame4, text="", width=50, font="Verdana 10 bold")
        lastLabel.grid(row=8, column=0, columnspan=2)


    def passwordCheck(lastLabel,newUserFrame3,inputPassword,newUser):
        
        result=newUser.getPassword(inputPassword.get())
        if result=="usernamePassword":
            lastLabel.destroy()
            lastLabel=Label(newUserFrame3, text="Your password cannot be your username", width=80, pady=20, font="Verdana 9 bold",fg="red")
            lastLabel.grid(row=3, column=0, columnspan=2)

        elif result=="invalidPassword":
            lastLabel.destroy()
            lastLabel1=Label(newUserFrame3, text="You must include at least one capital letter in your password.", width=80, font="Verdana 9 bold",fg="red")
            lastLabel1.grid(row=3, column=0, columnspan=2)
            lastLabel2=Label(newUserFrame3, text="You cannot use !,^,*,-,+,'comma' in your password", width=80, font="Verdana 9 bold",fg="red")
            lastLabel2.grid(row=4, column=0, columnspan=2)
            lastLabel2=Label(newUserFrame3, text="You must user one of @,£,& in your password", width=80, font="Verdana 9 bold",fg="red")
            lastLabel2.grid(row=5, column=0, columnspan=2)

        else:
            newUserFrame3.destroy()
            newOtherData(newUser)

    def newPassword(newUser):
        
        newUserFrame3=Frame(root, width=100, height=250)
        newUserFrame3.pack(fill="both", expand=True, padx=20, pady=20)
        newUserFrame3.place(in_=root, anchor="c", relx=.5, rely=.5)

        label1 = Label(newUserFrame3, text="Please enter your password", width=80, pady=20, font="Verdana 10 bold")
        label1.grid(row=0, column=0, columnspan=2)

        inputPassword = Entry(newUserFrame3, width=80)
        inputPassword.grid(row=2, column=0, columnspan=2)

        nextButton = Button(newUserFrame3, text="Next", width=20, command=lambda: passwordCheck(lastLabel,newUserFrame3,inputPassword,newUser))
        nextButton.grid(row=2, column=1, columnspan=2)

        lastLabel=Label(newUserFrame3, text="", width=80, pady=20, font="Verdana 10 bold")
        lastLabel.grid(row=3, column=0, columnspan=2)

    def usernameCheck(lastLabel,newUserFrame2,inputUsername,newUser):

        #getting previous usernames
        usernames=[]
        qurey=("SELECT username from users")
        cursor.execute(qurey)
        for i in cursor:
            for item in i:
                usernames.append(item)
        
        result=newUser.getUsername(inputUsername.get(),usernames)
        if result=="longUsername":
            lastLabel.destroy()
            lastLabel=Label(newUserFrame2, text="This username is long", width=80, pady=20, font="Verdana 9 bold",fg="red")
            lastLabel.grid(row=3, column=0, columnspan=2)

        elif result=="unavailableUsername":
            lastLabel.destroy()
            lastLabel=Label(newUserFrame2, text="This username is not available", width=80, pady=20, font="Verdana 9 bold",fg="red")
            lastLabel.grid(row=3, column=0, columnspan=2)

        else:
            newUserFrame2.destroy()
            newPassword(newUser)

    def username(newUser):

        newUserFrame2=Frame(root, width=100, height=250)
        newUserFrame2.pack(fill="both", expand=True, padx=20, pady=20)
        newUserFrame2.place(in_=root, anchor="c", relx=.5, rely=.5)

        label1 = Label(newUserFrame2, text="Please enter your username", width=80, pady=20, font="Verdana 10 bold")
        label1.grid(row=0, column=0, columnspan=2)

        inputUsername = Entry(newUserFrame2, width=80)
        inputUsername.grid(row=2, column=0, columnspan=2)

        nextButton = Button(newUserFrame2, text="Next", width=20, command=lambda: usernameCheck(lastLabel,newUserFrame2,inputUsername,newUser))
        nextButton.grid(row=2, column=1, columnspan=2)

        lastLabel=Label(newUserFrame2, text="", width=80, pady=20, font="Verdana 10 bold")
        lastLabel.grid(row=3, column=0, columnspan=2)

    def emailCheck(lastLabel,newUserFrame1, inputEmail,newUser):

            #getting previous emails
            exEmail=("SELECT email FROM users")
            cursor.execute(exEmail)
            emails=[]
            for item in cursor:
                for email in item:
                    emails.append(email)

            result=newUser.getEmail(inputEmail.get(),emails)
            if result=="invalidEmail":
                lastLabel.destroy()
                lastLabel=Label(newUserFrame1, text="Please enter a valid email", width=80, pady=20, font="Verdana 9 bold",fg="red")
                lastLabel.grid(row=3, column=0, columnspan=2)

            elif result=="existingEmail":
                lastLabel.destroy()
                lastLabel=Label(newUserFrame1, text="This email is already registered", width=80, pady=20, font="Verdana 9 bold",fg="red")
                lastLabel.grid(row=3, column=0, columnspan=2)

            else:
                newUserFrame1.destroy()
                username(newUser)

    def createUser(mainFrame):

        newUser=user()

        mainFrame.destroy()

        newUserFrame1=Frame(root, width=60, height=250)
        newUserFrame1.pack(fill="both", expand=True)
        newUserFrame1.place(in_=root, anchor="c", relx=.5, rely=.5)

        label1 = Label(newUserFrame1, text="Please enter your email", width=60, pady=20, font="Verdana 11 bold")
        label1.grid(row=0, column=0, columnspan=2)

        inputEmail = Entry(newUserFrame1, width=60)
        inputEmail.grid(row=2, column=0,columnspan=2)

        nextButton = Button(newUserFrame1, text="Next", width=20, command=lambda: emailCheck(lastLabel,newUserFrame1, inputEmail,newUser))
        nextButton.grid(row=2, column=1,columnspan=2)

        lastLabel=Label(newUserFrame1, text="", width=60, pady=20, font="Verdana 10 bold")
        lastLabel.grid(row=3, column=0, columnspan=2)


    def User_status_checker():
        mainFrame = Frame(root, width=500, height=250)
        mainFrame.pack(fill="both", expand=True, padx=20, pady=20)
        mainFrame.place(in_=root, anchor="c", relx=.5, rely=.5)

        label1 = Label(mainFrame, text="Do you have an existing account?", width=50, pady=20, font="Verdana 10 bold")
        label1.grid(row=0, column=0, columnspan=2)

        label2 = Label(mainFrame, text="", width=50)
        label2.grid(row=1, column=0, columnspan=2)

        yesButton = Button(mainFrame, text="Yes", width=20, command=lambda: exitingUser(mainFrame))
        yesButton.grid(row=2, column=0)

        noButton = Button(mainFrame, text="no", width=20, command= lambda: createUser(mainFrame))
        noButton.grid(row=2, column=1)

        label2 = Label(mainFrame, text="", width=50)
        label2.grid(row=3, column=0, columnspan=2)
        root.mainloop()
    User_status_checker()


main()