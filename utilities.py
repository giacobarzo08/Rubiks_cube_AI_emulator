import ctypes
import pygame as pg
import logging
import platform
from math import sqrt

# returns the value scaled to the current screen resolution
def val(value: int) -> int:
    if not isinstance(value, int):
        logging.error("Value must be an integer.")
        raise TypeError("Value must be an integer.")
    if value < 0:
        logging.error("Value must be a non-negative integer.")
        raise ValueError("Value must be a non-negative integer.")
    
    width = ctypes.windll.user32.GetSystemMetrics(0)
    return int(value * width / 1920)


# insert a message in the Pygame window
def get_message(message: str,
                x: int, y: int,
                surface: pg.Surface,
                color: tuple[int, int, int] = (0, 0, 0)) -> None:
    """
    Displays a message in a Pygame window.
    """
    try:
        font = pg.font.Font(None, 36)
        text = font.render(message, True, color)
        text_rect = text.get_rect(center=(x, y))
        surface.blit(text, text_rect)
    except Exception as e:
        logging.critical(f"Error displaying message: {e}", exc_info=True)
        raise RuntimeError("Failed to display message in Pygame window.") from e

# A class to represent a rectangle with a color attribute
class PyRect():
    def __init__(self, color: tuple[int, int, int]) -> None:
        if not isinstance(color, tuple) or len(color) != 3:
            logging.error("Color must be a tuple of three integers.")
            raise TypeError("Color must be a tuple of three integers.")
        self._color = color
    
    @property
    def color(self) -> tuple[int, int, int]:
        return self._color

def veryfy_circle(centr: tuple[int, int], coor: tuple[int, int], radius: int) -> None:
    """
    Verifies if the coordinates are within the bounds of a circle.
    """
    if not isinstance(centr, tuple) or len(centr) != 2:
        raise TypeError("Center coordinates must be a tuple of two integers.")
    if not isinstance(coor, tuple) or len(coor) != 2:
        raise TypeError("Coordinates must be a tuple of two integers.")
    if not isinstance(radius, int) or radius <= 0:
        raise ValueError("Radius must be a positive integer.")
    
    x, y = coor
    x_c, y_c = centr
    if sqrt((x - x_c) ** 2 + (y - y_c) ** 2) < radius:
        return True
    else:
        return False

def ancora_in_sviluppo() -> str:
    if platform.system() == 'Windows':
        tmp = "\n========================================================================================\n"
        tmp += "Feature still in development, please check the GitHub repository for updates.\n"
        tmp += "wiew our progress cloning our latest reperstory\n"
        tmp += "winget installa git\n"
        tmp += "git clone ssh://git@github.com/giacobarzo08/cubo-di-rubik.git\n"
        tmp += "========================================================================================\n"
        return tmp
    elif platform.system() == 'Linux':
        tmp = "\n========================================================================================\n"
        tmp += "Feature still in development, please check the GitHub repository for updates.\n"
        tmp += "wiew our progress cloning our latest reperstory\n"
        tmp += "sudo apt update && sudo apt install -y git\n"
        tmp += "git clone ssh://git@github.com/giacobarzo08/cubo-di-rubik.git\n"
        tmp += "========================================================================================\n"
        return tmp

def AI_is_running(surface: pg.surface) -> bool:
    surface.fill((255, 255, 255))
    get_message("NON CHIUDERE QUESTA FINESTRA per evitare di incorrere in errori", val(960), val(540), surface, (255, 0, 0))
    get_message("Guarda la console di comando per vedere i progressi dell'AI", val(960), val(580), surface)
    get_message("Puoi interrompere il codice di AI in qualsiasi momento digitando Ctrl+C nel terminale", val(960), val(620), surface)
    get_message("Alla chiusura del programma AI quasto display verrà chiuso automaticamente", val(960), val(660), surface)