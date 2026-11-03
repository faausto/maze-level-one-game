import sqlite3
import db

DB = "ranking.db"

db.init_db()

con = sqlite3.connect(DB)
con.execute("INSERT INTO puntajes (nombre, puntaje) VALUES (?, ?)", ("Ana", 1500))
con.execute("INSERT INTO puntajes (nombre, puntaje) VALUES (?, ?)", ("Luis", 2300))
con.execute("INSERT INTO puntajes (nombre, puntaje) VALUES (?, ?)", ("Sofia", 1800))
con.commit()

cur = con.execute("SELECT nombre, puntaje FROM puntajes ORDER BY puntaje DESC LIMIT 3")
for nombre, puntaje in cur.fetchall():
    print(nombre, puntaje)

con.close()
