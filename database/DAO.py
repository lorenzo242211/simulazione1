from database.DB_connect import DBConnect
from model.artista import Artista

class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getGeneri():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from Genre"""

        cursor.execute(query)
        for row in cursor:
            result.append((row["GenreId"], row["Name"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodi(genere):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT a.ArtistId, a.Name
            FROM Artist a
            JOIN Album alb ON a.ArtistId = alb.ArtistId
            JOIN Track t ON alb.AlbumId = t.AlbumId
            WHERE t.GenreId = %s"""
            #ho usato le join molto comode, aggiungo incrocio gli if di altre tabelle in questo caso
            #se artista album coincide con artista canzone e album id coincide con traccia album id
            #faccio la where totale su se traccia genere = genere utente
        cursor.execute(query, (genere,))
        for row in cursor:
            result.append(Artista(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPop():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT a.ArtistId, SUM(il.Quantity) as popolarita
FROM Artist a
JOIN Album al ON a.ArtistId = al.ArtistId
JOIN Track t ON al.AlbumId = t.AlbumId
JOIN InvoiceLine il ON t.TrackId = il.TrackId
GROUP BY a.ArtistId"""
        cursor.execute(query)
        for row in cursor:
            result.append((row["ArtistId"], row["popolarita"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi(genere):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT  i.CustomerId, a.ArtistId
FROM InvoiceLine il 
JOIN Invoice i ON il.InvoiceId = il.InvoiceId 
JOIN Track t ON il.TrackId = t.TrackId
JOIN Album a ON a.AlbumId = t.AlbumId
where t.GenreId = %s
"""

        cursor.execute(query, (genere,))
        for row in cursor:
            result.append((row["CustomerId"], row["ArtistId"]))

        cursor.close()
        conn.close()
        return result
