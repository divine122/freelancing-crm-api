#install mySql on my computer
#pip install mysql
#pip install mysql-connector
#pip install mysql-connector-python
#https://dev.mysql.com/downloads/installer

#'Z3n&Qw8m!Jp4vR9',

import pymysql

# Connect to MySQL
dataBase = pymysql.connect(
    host='localhost',
    user='root',
    password='Z3n&Qw8m!Jp4vR9',
)

# Prepare a cursor object
cursorObject = dataBase.cursor()

# Create a database
cursorObject.execute("CREATE DATABASE IF NOT EXISTS deecode")

print("✅ Database 'deecode' created successfully!")


