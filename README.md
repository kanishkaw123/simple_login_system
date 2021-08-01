# Simple Login System

This is a simple Python - MySQL database which consist of a Tlinter GUI. This programme allows users to create accounts and store data on a MySQL database securely and conveniently. 

## Installation
1. First download MySQL and MySQL Connector.
2. Download Login_System_Install.zip file.
3. Unzip it to a preffered location in your local drive.
4. Edit the **conn.data** file as shown below.
    - Replace line 1 with your MySQL host IP address.
    - Replace line 2 with your MySQL username.
    - Replace line 3 with your MySQL password.
5. Do not change the **database.name**.
6. Now run the programme. The programme must automatically create the database

###### If the database isn't created automatically, do the following steps.

1. Create a database useing this command : `create database user_data;`
2. Create a new table using the code snippet shown below.

   ` create table users (
      user_id int not null primary key auto_increment, 
      firstname varchar(30) not null, 
      surname varchar(40) not null, 
      email varchar(70) not null,
      username varchar(20) not null,
      password varchar(16) not null,
      data text null);`

3. Recommended: Set the initial value for 'user_id' with this command:  `alter table users auto_increment=1000; `
