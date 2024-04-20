import pygame as pg
import gui

WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 800

SEARCH_BAR_HEIGHT = 50

def start_pathing():
    print("Starting Pathing")

def run():
    pg.init()
    win = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.display.set_caption("TribeHacks 2024 -- Maps")
    font = pg.font.SysFont("arial", 30)

    buildings = [
        "Griffin",
        "Swem",
        "Sadler"
    ]

    # making sprites
    half_green_half_gold = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.draw.rect(half_green_half_gold, (19, 98, 7), pg.Rect(0, 0, WINDOW_WIDTH/2, WINDOW_HEIGHT))
    pg.draw.rect(half_green_half_gold, (212, 175, 55), pg.Rect(WINDOW_WIDTH/2, 0, WINDOW_WIDTH/2, WINDOW_HEIGHT))
    btn_sprite = pg.Surface((56, 35))
    btn_sprite.fill((122, 122, 122))
    btn_sprite.blit(font.render("Go!", True, (0, 0, 0), (122,122,122)),(5, 0))
    btn_rect = btn_sprite.get_rect().move(1000, 10)

    # gui elements
    view = gui.ScrollingImage(pg.Rect(0.0, SEARCH_BAR_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT), pg.image.load("map.png"))
    start_text = gui.Text([160.0, 10.0], "From:", font)
    start_input = gui.SearchBar(pg.Rect(250.0, 15.0, 200.0, 25.0), "Building Name", buildings)
    end_text = gui.Text([650, 10.0], "To:", font)
    end_input = gui.SearchBar(pg.Rect(700.0, 15.0, 200.0, 25.0), "Building Name", buildings)
    finished_button = gui.Button(btn_rect, btn_sprite, start_pathing)
    search_frame = gui.Frame(pg.Rect(0.0, 0.0, WINDOW_WIDTH, SEARCH_BAR_HEIGHT), half_green_half_gold, start_text, start_input, end_text, end_input, finished_button)
    elements = [view, search_frame]

    # logic operators
    mouse_down = False
    scoped_element = gui.BlankElement()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mpos = [event.pos[0], abs(event.pos[1] - WINDOW_HEIGHT)]
                if not scoped_element.was_pressed(mpos):
                    for el in elements:
                        if el.was_pressed(mpos):
                            scoped_element = el
                            break
                scoped_element.on_click(mpos)
                mouse_down = True
            elif event.type == pg.MOUSEBUTTONUP:
                mouse_down = False
            elif event.type == pg.KEYDOWN:
                scoped_element.key_press(event)

        mpos = pg.mouse.get_pos()
        dmpos = pg.mouse.get_rel()        
        scoped_element.mouse_movement(mouse_down, dmpos[0], dmpos[1])

        win.fill((255,255,255))
        for el in elements:
            win.blit(el.surface, [el.rect.left, WINDOW_HEIGHT - el.rect.bottom])
        pg.display.flip()