"""Persistencia local del ranking de puntuaciones en SQLite."""

import logging
import sqlite3
from contextlib import closing
from datetime import datetime

from src.constants import DATABASE_DIR

logger = logging.getLogger(__name__)

RUTA_DB = DATABASE_DIR / "ranking.db"


class Database:
    """Acceso al ranking: crea la tabla, lee el Top 10 y guarda puntajes."""

    def __init__(self):
        RUTA_DB.parent.mkdir(parents=True, exist_ok=True)
        self.ranking = []
        self._crear_tabla()
        self.cargar_ranking()

    def _conectar(self):
        return closing(sqlite3.connect(RUTA_DB))

    def _crear_tabla(self):
        with self._conectar() as conn, conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS ranking ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "nombre TEXT NOT NULL, "
                "puntaje INTEGER NOT NULL, "
                "fecha TEXT NOT NULL)"
            )

    def cargar_ranking(self):
        """Carga en memoria el Top 10 ordenado por puntaje."""
        try:
            with self._conectar() as conn:
                filas = conn.execute(
                    "SELECT nombre, puntaje FROM ranking "
                    "ORDER BY puntaje DESC LIMIT 10"
                ).fetchall()
            self.ranking = [
                {"nombre": nombre, "puntaje": puntaje}
                for nombre, puntaje in filas
            ]
        except sqlite3.Error as error:
            logger.error("No se pudo leer el ranking: %s", error)
            self.ranking = []

    def guardar_puntaje(self, nombre, puntaje):
        """Guarda un puntaje. Devuelve True si se guardó correctamente."""
        nombre = nombre.strip()[:15]
        if not nombre:
            return False
        try:
            with self._conectar() as conn, conn:
                conn.execute(
                    "INSERT INTO ranking (nombre, puntaje, fecha) "
                    "VALUES (?, ?, ?)",
                    (
                        nombre,
                        int(puntaje),
                        datetime.now().strftime("%Y-%m-%d %H:%M"),
                    ),
                )
        except sqlite3.Error as error:
            logger.error("No se pudo guardar el puntaje: %s", error)
            return False
        self.cargar_ranking()
        return True
