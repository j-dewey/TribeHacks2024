import pygame as pg
from lib import gui
from lib import map_editor
from lib import graph

WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 800

EDIT_BAR_WIDTH = 400

SEARCH_BAR_HEIGHT = 50

'''
    Look for a path from the selection in start to the selection in end
    Returns early if an unrecognized buliding name is entered
'''
def start_pathing(start: gui.SearchBar, end: gui.SearchBar, map: gui.ScrollingImage, overlay: gui.ScrollingImage, building_list: list[str]):
    if not start.input in building_list or not end.input in building_list:
        return

    start_node = map_editor.traversal_nodes[start.input]
    end_node = map_editor.traversal_nodes[end.input]
    path = graph.reverse_traversal(start_node, graph.alt_traverse_node(start_node, end_node))
    map_editor.draw_path(path)

    # Center on start node
    node_coords = start_node.gui_inter.coords
    desired_pos = [WINDOW_WIDTH / 2.0, (WINDOW_HEIGHT - SEARCH_BAR_HEIGHT) / 2.0]
    if node_coords[0] < desired_pos[0]: desired_pos[0] = 0.0
    if node_coords[1] < desired_pos[1]: desired_pos[1] = 0.0
    dx = desired_pos[0] - node_coords[0]
    dy = desired_pos[1] - node_coords[1]
    map.offset = [dx, dy]

    map.render()
    overlay.offset = [dx, dy]
    overlay.render()

'''
    Main Loop
'''
def run(edit_mode: bool, asset_path: str):
    pg.init()
    if edit_mode:
        win = pg.display.set_mode((WINDOW_WIDTH + EDIT_BAR_WIDTH, WINDOW_HEIGHT))
    else:
        win = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.display.set_caption("TribeHacks 2024 -- Maps")

    font = pg.font.SysFont("arial", 30)
    mid_font = pg.font.SysFont("arial", 20)
    small_font = pg.font.SysFont("arial", 10)

    # making sprites
    half_green_half_gold = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.draw.rect(half_green_half_gold, (19, 98, 7), pg.Rect(0, 0, WINDOW_WIDTH/2, WINDOW_HEIGHT))
    pg.draw.rect(half_green_half_gold, (212, 175, 55), pg.Rect(WINDOW_WIDTH/2, 0, WINDOW_WIDTH/2, WINDOW_HEIGHT))
    half_green_half_gold.blit(small_font.render("Map Courtesy of OpenStreetMap", True, (0,0,0)), (WINDOW_WIDTH - 175, 35.0))
    btn_sprite = pg.Surface((56, 30))
    btn_sprite.fill((122, 122, 122))
    btn_sprite.blit(mid_font.render("Go!", True, (0, 0, 0), (122,122,122)),(10, 2))
    btn_rect = btn_sprite.get_rect().move(1000, 5)

    # gui elements
    view = gui.ScrollingImage(pg.Rect(0.0, SEARCH_BAR_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT), pg.image.load(asset_path + "map.png"), [-943, -545])
    overlay_image = pg.Surface(view.image.get_size(), pg.SRCALPHA)
    editor_overlay = gui.ScrollingImage(view.rect, overlay_image, view.offset)

    # prepping editor
    map_editor.load_things(view, editor_overlay, WINDOW_HEIGHT, asset_path)
    view.mouse_movement = map_editor.scrolling_image_mouse_move_override
    building_list = list(map_editor.traversal_nodes.keys())

    # create the bottom bar
    start_text = gui.Text([160.0, 10.0], "From:", font)
    end_text = gui.Text([650, 10.0], "To:", font)
    start_input = gui.SearchBar(pg.Rect(250.0, 15.0, 200.0, 25.0), "Building Name", building_list)
    end_input = gui.SearchBar(pg.Rect(700.0, 15.0, 200.0, 25.0), "Building Name", building_list)
    finished_button = gui.Button(btn_rect, btn_sprite, lambda: start_pathing(start_input, end_input, view, editor_overlay, building_list))

    # load elements int containers
    search_frame = gui.Frame(pg.Rect(0.0, 0.0, WINDOW_WIDTH, SEARCH_BAR_HEIGHT), half_green_half_gold, start_text, start_input, end_text, end_input, finished_button)
    elements = [view, search_frame, editor_overlay]

    # edit mode stuff
    if edit_mode:
        mode_btn_sprite = font.render("Mode: Vertex", True, (255, 255, 255), (122, 122, 122))
        mode_btn = gui.Button(mode_btn_sprite.get_rect().move(WINDOW_WIDTH, WINDOW_HEIGHT - mode_btn_sprite.get_height()), mode_btn_sprite, lambda a: ... )
        mode_btn.onclick = lambda: map_editor.toggle_edit_mode(mode_btn, font)

        save_btn_sprite = font.render("Save", True, (255, 255, 255), (122, 122, 122))
        save_btn = gui.Button(save_btn_sprite.get_rect().move(WINDOW_WIDTH, 0), save_btn_sprite, map_editor.save_map_data)

        view.on_click = map_editor.scrolling_image_on_click_override

        vertex_frame = map_editor.generate_vertex_edit_frame(WINDOW_WIDTH, EDIT_BAR_WIDTH)
        elements += [mode_btn, vertex_frame, save_btn]

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
        map_editor.overlay_overlay()
        for el in elements:
            win.blit(el.surface, [el.rect.left, WINDOW_HEIGHT - el.rect.bottom])
        pg.display.flip()
