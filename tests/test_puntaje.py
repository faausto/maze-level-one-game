"""Tests del cálculo de puntajes (RF-16)."""

from src.scoring import calcular_bonus


def test_bonus_victoria():
    assert calcular_bonus(vidas=3, segundos_restantes=40) == 100 + 150 + 200


def test_bonus_usa_los_segundos_sobrantes():
    # 5 vidas y 29 segundos: 100 + 5*50 + 29*5 = 495.
    assert calcular_bonus(vidas=5, segundos_restantes=29) == 495


def test_bonus_trunca_los_segundos():
    assert calcular_bonus(vidas=0, segundos_restantes=9.9) == 100 + 45
