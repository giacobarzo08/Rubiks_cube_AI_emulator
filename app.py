import ctypes
import ctypes.wintypes
import pygame as pg
import numpy as np
import logging
import subprocess
import sys
from cube_status import Cube
from utilities import *
from plots import RubikCubePlotter
from copy import deepcopy

class Display:
    def __init__(self,) -> None:
        try:
            pg.init()

            SPI_GETWORKAREA = 48
            rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0)

            self.virtual_width = rect.right - rect.left
            self.virtual_height = rect.bottom - rect.top
            self.virtual_surface = pg.Surface((self.virtual_width, self.virtual_height))
            self.virtual_surface.fill((255, 255, 255))

            self.screen = pg.display.set_mode((self.virtual_width, self.virtual_height), pg.RESIZABLE)
            self.clock = pg.time.Clock()
            pg.display.set_caption("Il cubo di Rubik")
            self.screen.fill((255, 255, 255))  # Fill the screen with black
            self.clock.tick(30)  # Limit to 30 FPS

            self.scaled_surface = self.virtual_surface
            self.scaled_size = (self.virtual_width, self.virtual_height)

            pg.display.flip()
            logging.info("Display initialized successfully.")
        except Exception as e:
            logging.critical(f"Error initializing Display: {e}", exc_info=True)
            sys.exit('critical error in Display initialization, exiting...')
    

    def show_face(self, number: int, rects = np.ndarray[PyRect]) -> None:
        if not isinstance(number, int) or not (1 <= number <= 6):
            logging.error("Number must be an integer between 1 and 6.")
            raise ValueError("Number must be an integer between 1 and 6.")
        
        if not isinstance(rects, np.ndarray) or rects.dtype != PyRect:
            logging.error("rects must be a numpy ndarray of PyRect objects.")
            raise TypeError("rects must be a numpy ndarray of PyRect objects.")
        
        if len(rects) != 9:
            logging.error("rects must contain exactly 9 PyRect objects.")
            raise ValueError("rects must contain exactly 9 PyRect objects.")

        rect_dimension = val(80)
        location = {
            1: (val(295), val(72)),
            2: (val(835), val(72)),
            3: (val(1380), val(72)),
            4: (val(295), val(390)),
            5: (val(835), val(390)),
            6: (val(1380), val(390))
        }

        try:
            x_0, y = location.get(number)
            x = x_0
            for rect in rects[:3]:
                # Disegna su self.virtual_surface invece di self.screen
                pg.draw.rect(self.virtual_surface, rect.color, (x, y, rect_dimension, rect_dimension))
                pg.draw.rect(self.virtual_surface, (0, 0, 0), (x, y, rect_dimension, rect_dimension), val(2))
                x += rect_dimension
            y += rect_dimension
            x = x_0
            for rect in rects[3:6]:
                pg.draw.rect(self.virtual_surface, rect.color, (x, y, rect_dimension, rect_dimension))
                pg.draw.rect(self.virtual_surface, (0, 0, 0), (x, y, rect_dimension, rect_dimension), val(2))
                x += rect_dimension
            y += rect_dimension
            x = x_0
            for rect in rects[6:]:
                pg.draw.rect(self.virtual_surface, rect.color, (x, y, rect_dimension, rect_dimension))
                pg.draw.rect(self.virtual_surface, (0, 0, 0), (x, y, rect_dimension, rect_dimension), val(2))
                x += rect_dimension
            logging.info(f"Face {number} displayed successfully.")

        except Exception as e:
            logging.critical(f"Error in show_face: {e}", exc_info=True)
            sys.exit('critical error in show_face, exiting...')
    
    def show_cube(self, cube: Cube) -> None:
        j = 1
        colors = {
            'w': (255, 255, 255),  
            'b': (0, 0, 255),      
            'o': (255, 165, 0),    
            'g': (0, 128, 0),      
            'r': (255, 0, 0),      
            'y': (255, 255, 0),    
        }
        for _ in ('U', 'F', 'R', 'B', 'L', 'D'):
            c = []
            for i in [f'{_}{n}' for n in range(1, 10)]:
                color = colors[cube.blocks[i]]
                c.append(PyRect(color))
            self.show_face(j, np.array(c, dtype=object))
            j+= 1
    
    def new_cube(self):
        self.show_cube(Cube())
    
    def buttons(self) -> None:
        # Draw the buttons on the virtual surface
        self.rects = []
        colors = [(255, 0, 0), (0, 255, 2)]
        words = ["U'", "F'", "R'", "B'", "L'", "D'", "U", "F", "R", "B", "L", "D"]
        y = val(723)
        
        try:
            for i in range(2):
                x = val(80)
                for _ in range(6):
                    rect = pg.Rect(x, y, val(139), val(117))
                    self.rects.append(rect)
                    pg.draw.rect(self.virtual_surface, colors[i], rect)
                    x += val(211)
                y += val(139)
        except Exception as e:
            logging.critical(f"Error in buttons: {e}", exc_info=True)
            sys.exit('critical error in buttons, exiting...')
        
        # Draw the text on the buttons
        try:
            for rect in self.rects:
                get_message(words[self.rects.index(rect)],
                            rect.centerx, rect.centery,
                            self.virtual_surface)
        except Exception as e:
            logging.critical(f"Error in buttons text: {e}", exc_info=True)
            sys.exit('critical error in buttons text, exiting...')
        
    def inizialize(self) -> None:
        self.virtual_cube = Cube()
        self.new_cube() # Disegna il cubo sulla virtual_surface una volta
        
        # Show the name of the faces
        get_message("U", val(239), val(195), self.virtual_surface)
        get_message("F", val(779), val(195), self.virtual_surface)
        get_message("R", val(1324), val(195), self.virtual_surface)
        get_message("B", val(239), val(513), self.virtual_surface)
        get_message("L", val(779), val(513), self.virtual_surface)
        get_message("D", val(1324), val(513), self.virtual_surface)

        self.buttons()  # Disegna i bottoni sulla virtual_surface
        pg.draw.circle(self.virtual_surface, (0, 0, 255), (val(1456), val(851)), val(111))
        get_message("3D Cube Plot", val(1456), val(851), self.virtual_surface)
        pg.draw.circle(self.virtual_surface, (0, 0, 255), (val(1736), val(851)), val(111))
        get_message("AI Solving", val(1736), val(851), self.virtual_surface)
        
    def run(self) -> None:
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.VIDEORESIZE:
                    self.scaled_size = event.w, event.h
                elif event.type == pg.KEYDOWN:
                    if pg.K_a <= event.key <= pg.K_z:
                        if event.key == pg.K_q:
                            if pg.key.get_mods() & pg.KMOD_CTRL:
                                running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    for rect in self.rects:
                        if rect.collidepoint(event.pos):
                            index = self.rects.index(rect)
                            if index < 6:
                                self.virtual_cube.rotate_face(index + 1, counter_clockwise=True)
                            else:
                                self.virtual_cube.rotate_face(index - 5, counter_clockwise=False)
                            self.show_cube(self.virtual_cube)
                    if veryfy_circle((val(1456), val(851)), event.pos, val(111)):
                        plt = RubikCubePlotter(self.virtual_cube)
                        plt.plot_cube()
                    if veryfy_circle((val(1736), val(851)), event.pos, val(111)):
                        copied_cube = deepcopy(self.virtual_cube._blocks)
                        with open('cube.py', 'w') as f:
                            f.write(f'my_rubiks_cube_state = {copied_cube}')
                        subprocess.Popen('python ai_learner.py --load_model --inference --load_cube=cube.py', shell=True)
                        AI_is_running(self.virtual_surface)

            self.screen.fill((255, 255, 255))
            self.scaled_surface = pg.transform.scale(self.virtual_surface, self.scaled_size)
            self.screen.blit(self.scaled_surface, (0, 0))
            pg.display.flip()
            self.clock.tick(30)

        pg.quit()

if __name__ == "__main__":
    display = Display()
    display.inizialize()
    display.run()