#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database. Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    set_wins_to_zero_query = "UPDATE players SET wins = 0;"
    set_matches_to_zero_query = "UPDATE players SET matches = 0;"
    remove_matches_query = "DELETE FROM matches;"
    conn = connect()
    c = conn.cursor()
    c.execute(set_wins_to_zero_query)
    c.execute(set_matches_to_zero_query)
    c.execute(remove_matches_query)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    remove_matches_query = "DELETE FROM matches;"
    remove_players_query = 'DELETE FROM players;'
    conn = connect()
    c = conn.cursor()
    c.execute(remove_matches_query)
    c.execute(remove_players_query)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    query = 'SELECT COUNT(player_id) as NUM FROM players;'
    conn = connect()
    c = conn.cursor()
    c.execute(query)
    result = int(c.fetchone()[0])
    conn.commit()
    conn.close()
    return result


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    query = 'INSERT INTO players (name) VALUES (%s);'
    conn = connect()
    c = conn.cursor()
    c.execute(query, (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    query = 'SELECT * FROM players ORDER BY wins DESC;'
    conn = connect()
    c = conn.cursor()
    c.execute(query)
    result = c.fetchall()
    conn.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    add_match_query = 'INSERT INTO matches (winner_id, loser_id) VALUES ({0}, {1});'.format(winner, loser)
    add_winner_query = 'UPDATE players SET matches=matches+1, wins=wins+1 WHERE player_id = {0};'.format(winner)
    add_loser_query = 'UPDATE players SET matches=matches+1 WHERE player_id = {0};'.format(loser)
    conn = connect()
    c = conn.cursor()
    c.execute(add_match_query)
    c.execute(add_winner_query)
    c.execute(add_loser_query)
    conn.commit()
    conn.close()

 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairings = []
    players = playerStandings()
    if len(players) < 2:
        raise KeyError("Not enough players.")
    for i in range(0, len(players), 2):
        pairings.append((players[i][0], players[i][1], players[i+1][0], players[i+1][1]))
    return pairings
