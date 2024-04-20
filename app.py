import pygame as pg

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

def run():
    win = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.display.set_caption("TribeHacks 2024 -- Maps")

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
        
        pg.display.flip()