"""Punto de entrada del juego."""

import logging

from src.game import Juego


def main():
    """Configura el registro de eventos y arranca el juego."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )
    Juego().ejecutar()


if __name__ == "__main__":
    main()
