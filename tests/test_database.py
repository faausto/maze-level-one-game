"""Tests de la base de datos del ranking."""

from src.db import database


def test_top_10_ordenado(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "RUTA_DB", tmp_path / "test.db")
    db = database.Database()

    for i in range(12):
        assert db.guardar_puntaje(f"J{i}", i * 10)

    assert len(db.ranking) == 10
    assert db.ranking[0]["puntaje"] == 110
    assert db.ranking == sorted(
        db.ranking, key=lambda entrada: entrada["puntaje"], reverse=True
    )


def test_nombre_vacio_no_se_guarda(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "RUTA_DB", tmp_path / "test.db")
    db = database.Database()

    assert db.guardar_puntaje("   ", 100) is False
    assert db.ranking == []


def test_ruta_por_defecto_es_absoluta():
    assert database.RUTA_DB.is_absolute()
