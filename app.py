import pygame as pg
import gui

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

def run():
    win = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.display.set_caption("TribeHacks 2024 -- Maps")

    # gui elements
    view = gui.ScrollingImage(pg.Rect(0.0, 0.0, WINDOW_WIDTH, WINDOW_HEIGHT), pg.image.load("images/puppies.jpg"))
    elements = [view]

    # logic operators
    mouse_down = False
    scoped_element = gui.BlankElement()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if not scoped_element.was_pressed(event.pos):
                    for el in elements:
                        if el.was_pressed(event.pos):
                            scoped_element = el
                            break
                mouse_down = True
            elif event.type == pg.MOUSEBUTTONUP:
                mouse_down = False

        mpos = pg.mouse.get_pos()
        dmpos = pg.mouse.get_rel()        
        scoped_element.mouse_movement(mouse_down, dmpos[0], dmpos[1])

        win.fill((255,255,255))
        win.blit(view.surface, (0,0))
        pg.display.flip()