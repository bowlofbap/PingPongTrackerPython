# Python 3 program for Elo Rating 
import psycopg2
import math 
import sys

def getAllPlayers():
    sqlString = "SELECT * FROM players order by rating desc"
    try:
        connection = psycopg2.connect(user = "postgres",
                                    password = "postgres1",
                                    host = "localhost",
                                    port = "5432",
                                    database = "ratingTest")
        cursor = connection.cursor()
        cursor.execute(sqlString)
        players = cursor.fetchall()
        for player in players:
            print(player)

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                
if __name__ == '__main__':
    getAllPlayers()
    
