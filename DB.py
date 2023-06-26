import sqlite3
from sqlite3 import Error


def create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect("GoFundMeDatabase.db")
    except Error as e:
        print(e)

    return conn


def insert_fundraiser_data(conn, record):
    """ ïnserts first hand fundraiser data """
    sql = "INSERT INTO Fundraisers(Title,Location,Goal,RaisedMoney,Webpage,Image) VALUES(?,?,?,?,?,?)"
    cur = conn.cursor()
    cur.execute(sql, record)
    conn.commit()


def update_fundraiser_record(conn, record, id):
    sql = 'UPDATE Fundraisers SET Organizer = ?,DateCreated = ?,NrDonations = ?,Description = ?,NrUpdates = ?,' \
          'NrComments = ?,NrDonors = ?,Shares = ?, Followers = ?, Timestamp = ? WHERE id = {}'.format(id)
    cur = conn.cursor()
    cur.execute(sql, record)
    conn.commit()


def select_records(conn, sql):
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()
