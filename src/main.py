"""Punto de entrada del juego."""

import logging

from src.constants import CONGELADO, DATOS_USUARIO_DIR
from src.game import Juego

logger = logging.getLogger(__name__)


def main():
    """Configura el registro de eventos y arranca el juego."""
    if CONGELADO:
        DATOS_USUARIO_DIR.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s: %(message)s",
            handlers=[
                logging.FileHandler(
                    DATOS_USUARIO_DIR / "juego.log", encoding="utf-8"
                )
            ],
        )
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(levelname)s: %(message)s",
        )

    try:
        Juego().ejecutar()
    except Exception:
        logger.exception("Error no controlado al ejecutar el juego")
        raise


if __name__ == "__main__":
    main()
