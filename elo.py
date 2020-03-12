# Python 3 program for Elo Rating 
import psycopg2
import math 
import sys

# Function to calculate the Probability 
def Probability(rating1, rating2): 
	return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400)) 

# Function to calculate Elo rating 
# K is a constant. 
# d determines whether 
# Player A wins or Player B. 
def EloRating(Ra, Rb, Sa, Sb, K): 
    Sa = int(Sa)
    Sb = int(Sb)

    # To calculate the Winning 
    # Probability of Player B 
    Pb = Probability(Ra, Rb) 

    # To calculate the Winning 
    # Probability of Player A 
    Pa = Probability(Rb, Ra) 

    # Case -1 When Player A wins 
    # Updating the Elo Ratings 
    if (Sa > Sb):
        print("player 1 won the game")
        Ra = Ra + K * (1 - Pa) 
        Rb = Rb + K * (0 - Pb) 
	

	# Case -2 When Player B wins 
	# Updating the Elo Ratings 
    else : 
        print("player 2 won the game")
        Ra = Ra + K * (0 - Pa) 
        Rb = Rb + K * (1 - Pb) 
    print("Updated Ratings:-") 
    print("Ra =", round(Ra, 6)," Rb =", round(Rb, 6)) 
    return Ra, Rb

# Driver code 

# Ra and Rb are current ELO ratings 
K = 30

def getPlayerFromUsername(username):
    sqlString = "SELECT * FROM players WHERE username = %s"
    player = None
    try:
        connection = psycopg2.connect(user = "postgres",
                                    password = "postgres1",
                                    host = "localhost",
                                    port = "5432",
                                    database = "ratingTest")

        cursor = connection.cursor()
        cursor.execute(sqlString, (username,))
        player = cursor.fetchone()

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()

    return player


def insertNewPlayer(username, name):
    sqlString = "INSERT INTO players (username, name) values(%s, %s)"
    playerToInsert = (username, name)
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

def postNewMatch(score1, score2, oldElo1, oldElo2, newElo1, newElo2, player1Id, player2Id):
    try:
        connection = psycopg2.connect(user = "postgres",
                                    password = "postgres1",
                                    host = "localhost",
                                    port = "5432",
                                    database = "ratingTest")
        sqlString = "INSERT INTO matches (p1score, p2score, p1ratinginit, p2ratinginit, p1ratingend, p2ratingend) values(%s, %s, %s, %s, %s, %s) RETURNING id"
        matchToInsert = (score1, score2, oldElo1, oldElo2, newElo1, newElo2)
        cursor = connection.cursor()
        cursor.execute(sqlString, matchToInsert)
        matchId = cursor.fetchone()[0]
        sqlString2 = "INSERT INTO player_match(p1id, p2id, matchid) values(%s, %s, %s)"
        playersToInsert = (player1Id, player2Id, matchId)
        cursor.execute(sqlString2, playersToInsert)

        sqlPlayerString = "UPDATE players SET rating = %s WHERE id = %s"
        cursor.execute(sqlPlayerString, (newElo1, player1Id))
        cursor.execute(sqlPlayerString, (newElo2, player2Id))
        connection.commit()
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()

if __name__ == '__main__':
    player1=getPlayerFromUsername(sys.argv[1])
    player2=getPlayerFromUsername(sys.argv[2])
    score1=sys.argv[3]
    score2=sys.argv[4]
    oldElo1=float(player1[3])
    oldElo2=float(player2[3])
    newElo1, newElo2 = EloRating(oldElo1, oldElo2, score1, score2, K) 
    postNewMatch(score1, score2, oldElo1, oldElo2, newElo1, newElo2, player1[0], player2[0])
    
