# Python 3 program for Elo Rating 
import psycopg2
import math 
import sys

def insertNewPlayer(username, firstName, lastName):
    sqlString = "INSERT INTO players (username, name) values(%s, %s)"
    playerToInsert = (username, firstName + " " + lastName)
    try:
        connection = psycopg2.connect(user = "postgres",
                                    password = "postgres1",
                                    host = "localhost",
                                    port = "5432",
                                    database = "ratingTest")
        cursor = connection.cursor()
        cursor.execute(sqlString, playerToInsert)
        connection.commit()

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                
if __name__ == '__main__':
    username=(sys.argv[1])
    firstName=(sys.argv[2])
    lastName=(sys.argv[3])
    insertNewPlayer(username, firstName, lastName)
    
