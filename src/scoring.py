"""Cálculo de puntajes y bonus de victoria (RF-16)."""

from src.constants import BONUS_POR_SEGUNDO, BONUS_POR_VIDA, BONUS_VICTORIA


def calcular_bonus(vidas, segundos_restantes):
    """Devuelve el bonus de victoria según las vidas y los segundos sobrantes."""
    return (
        BONUS_VICTORIA
        + int(vidas) * BONUS_POR_VIDA
        + int(segundos_restantes) * BONUS_POR_SEGUNDO
    )
