import sqlite3
from datetime import datetime

RUTA_DB = "database/ranking.db"


class Database:
    def __init__(self):
        self.ranking = []
        self.cargar_ranking()

    def cargar_ranking(self):
        try:
            conn = sqlite3.connect(RUTA_DB)
            cursor = conn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS ranking (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, puntaje INTEGER NOT NULL, fecha TEXT NOT NULL)"
            )
            cursor.execute("SELECT nombre, puntaje FROM ranking ORDER BY puntaje DESC LIMIT 10")
            self.ranking = [{"nombre": row[0], "puntaje": row[1]} for row in cursor.fetchall()]
            conn.close()
        except Exception:
            self.ranking = []

    def guardar_puntaje(self, nombre, puntaje):
        try:
            conn = sqlite3.connect(RUTA_DB)
            cursor = conn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS ranking (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, puntaje INTEGER NOT NULL, fecha TEXT NOT NULL)"
            )
            cursor.execute(
                "INSERT INTO ranking (nombre, puntaje, fecha) VALUES (?, ?, ?)",
                (nombre, puntaje, datetime.now().strftime("%Y-%m-%d %H:%M")),
            )
            conn.commit()
            conn.close()
            self.cargar_ranking()
        except Exception:
            pass
