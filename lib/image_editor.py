import pygame as pg

'''
    A tooling script that was used to help size an image during production
'''

if __name__ == '__main__':
    win = pg.display.set_mode((1600, 1200))

    upper = pg.image.load("images/upper_map.png")
    upper_coords = [0.0, 0.0]
    lower = pg.image.load("images/lower_map.png")
    lower_coords = [0.0, 600]
    moving_top = False
    editing = True

    while True:
        for ev in pg.event.get():
            if ev.type == pg.QUIT: quit()
            if ev.type == pg.KEYDOWN:
                if ev.unicode == "c":
                    moving_top = not moving_top
                elif ev.unicode == "s":
                    height = abs(upper_coords[1]) + lower_coords[1] + upper.get_height()
                    surface = pg.Surface((upper.get_width() - abs(lower_coords[0]), height))
                    surface.blit(upper, [0, 0])
                    surface.blit(lower, [lower_coords[0], height - lower.get_height() - 20])
                    pg.image.save(surface, "new_map.png")
                    quit()
                elif ev.unicode == "v":
                    editing = not editing
        dmouse = pg.mouse.get_rel()
        if editing:
            if moving_top:
                upper_coords = [upper_coords[0] + dmouse[0], upper_coords[1] + dmouse[1]]
            else:
                lower_coords = [lower_coords[0] + dmouse[0], lower_coords[1] + dmouse[1]]

        win.fill((255, 255, 255))
        win.blit(upper, upper_coords)
        win.blit(lower ,lower_coords)
        pg.display.flip()
